#include <stdio.h>
#include <time.h>

#define BYTE_SIZE 8
#define WORD_SIZE_B 4
#define WORD_SIZE_b 32
const int MAX_LENGTH = 16 * 2;  // 2 * 512-bit blocks

static const unsigned long K[64] = {
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

//function signatures
void setByte(unsigned long *A,  int byteIndex, char byte );
int testStreamBit(unsigned long *A, int k);
void setStreamBit(unsigned long *A, int k);
void clearStreamBit(unsigned long *A, int index);
int testLongBit(unsigned long *A, int index);
void setLongBit(unsigned long *A, int index);
void clearLongBit(unsigned long *A, int index);
void setWord(unsigned long *A, long long bitIndex, unsigned long word);
unsigned long long setString( unsigned long *A,  long long length, char *string );
void sudoSHA256(unsigned long *stream, unsigned long long stringLength, unsigned long *H);
int isGreater_256b(unsigned long *hash, unsigned long *target);

int main() {

    //todo: what is transaction to be hashed and included in blockHeader
    char *blockHeader = "\x02\x00\x00\x00"
                        "\x17\x97\x5b\x97\xc1\x8e\xd1\xf7\xe2\x55\xad\xf2\x97\x59\x9b\x55\x33\x0e\xda\xb8\x78\x03\xc8\x17\x01\x00\x00\x00\x00\x00\x00\x00"
                        "\x17\x97\x5b\x97\xc1\x8e\xd1\xf7\xe2\x55\xad\xf2\x97\x59\x9b\x55\x33\x0e\xda\xb8\x78\x03\xc8\x17\x01\x00\x00\x00\x00\x00\x00\x00"
                        "\x35\x8b\x05\x53"
                        "\x53\x50\xf1\x19";

//    char *transaction = "abcd";
//    unsigned int transactionLength = 4;
    char *transaction = "4\x00";
    unsigned int transactionLength = 2;
    //todo: check assumption
    // ulong type is 4B, long long type is 8B
    // blockHeader length is 76 Bytes

    unsigned long hash[8];
    unsigned long target[8] = {0x10101010ul, 0x10101010ul, 0x10101010ul, 0x10101010ul,
                               0x10101010ul, 0x10101010ul, 0x10101010ul, 0x10101010ul};
    unsigned long nonce = 0ul;

    unsigned long stream[MAX_LENGTH];
    //todo: decide whether start with a zero-initialized stream or make bits zero like below
    int i = 0;
    for (; i < MAX_LENGTH; ++i) {
        stream[i] = 0ul;
    }


    clock_t begin = clock();
    unsigned long long streamLength = setString(stream, (long long)transactionLength, transaction);
    sudoSHA256(stream, streamLength, hash);

//    printf("hash value found for prev:\n");
//    i = 0;
//    for (; i < 8; ++i) {
//        printf("<%08lx> ", hash[i]);
//    }
//    printf("end hash value found for prev:\n");

    //todo: decide whether start with a zero-initialized stream or make bits zero like below
    //resetting stream array
    i = 0;
    for (; i < MAX_LENGTH; ++i) {
        stream[i] = 0ul;
    }
    streamLength = setString(stream, 76ll, blockHeader);
    //setting merkle root and nonce in stream array to be hashed
    i = 9;
    for (; i < 17; ++i) {
        stream[i] = hash[i-9];
        hash[i-9] = 0xfffffffful;   //resetting hash array
    }
    stream[19] = nonce;
    streamLength += 4;

    while(isGreater_256b(hash, target))
    {
        stream[19] = nonce;
        sudoSHA256(stream, streamLength, hash);

        ++nonce;

//        printf("hash value found:\n");
//        i = 0;
//        for (; i < 8; ++i) {
//            printf("<%08lx> ", hash[i]);
//        }
//        printf("for nonce: %d\n", nonce);
    }

    --nonce;

    clock_t end = clock();
    float time_spent = (float)(end - begin) / CLOCKS_PER_SEC;

    printf("nonce value found: %lu\n", nonce);
    printf("time spent in seconds: %f\n", time_spent);

    printf("hash value found:\n");
    i = 0;
    for (; i < 8; ++i) {
        printf("<%08lx> ", hash[i]);
    }
    printf("\n------------------------------------");


    /*
    // test sudoSHA256 function
    clock_t begin = clock();
    char *blockHeader = "abcd";
    unsigned long stream[MAX_LENGTH];
    //todo: decide whether start with a zero-initialized stream or make bits zero like below
    int i = 0;
    for (; i < MAX_LENGTH; ++i) {
        stream[i] = 0ul;
    }
    unsigned long long streamLength = setString(stream, 4ll, blockHeader);
    unsigned long Hash[MAX_LENGTH];
    sudoSHA256(stream, streamLength, Hash);

    clock_t end = clock();
    float time_spent = (float)(end - begin) / CLOCKS_PER_SEC;

    printf("time spent in seconds: %f\n", time_spent);
    i = 0;
    for (; i < 8; ++i) {
        printf("<%08lx> ", Hash[i]);
    }

    */

}

int isGreater_256b(unsigned long *hash, unsigned long *target){
    int i = 0;
    for (; i < 8; ++i) {
        if (hash[i] > target[i])
            return 1;
        if(hash[i] < target[i])
            return 0;
        if(i == 7 && hash[i] == target[i])
            return 0;
    }
    return 1;
}

void sudoSHA256(unsigned long *stream, unsigned long long stringLength, unsigned long *H) {
    unsigned long long bitIndex = stringLength*BYTE_SIZE;
    setStreamBit(stream, bitIndex);
    ++bitIndex;
    //start:adding zero-array padding
    //todo: decide whether start with a zero-initialized stream or make bits zero like below
    int numberOfZeros = 0;
    int temp = bitIndex % 512;
    if(temp  <= 448)
        numberOfZeros = 448 - temp;
    else
        numberOfZeros = 960 - temp;     // = 448 + 512 - temp
    while (numberOfZeros && (bitIndex % WORD_SIZE_b)){
        clearStreamBit(stream, bitIndex);
        ++bitIndex;
        --numberOfZeros;
    }
    int numberOfWords = numberOfZeros/WORD_SIZE_b;
    numberOfZeros -= numberOfWords*WORD_SIZE_b;
    while (numberOfWords){
        setWord(stream, bitIndex, 0ul);
        bitIndex += WORD_SIZE_b;
        --numberOfWords;
    }
    while (numberOfZeros){
        clearStreamBit(stream, bitIndex);
        ++bitIndex;
        --numberOfZeros;
    }
    //end:adding zero-array padding
    //start: adding length field
    unsigned long long stringLength_b = stringLength*BYTE_SIZE;
    //leftmost 32 bits
    unsigned long split = (unsigned long)(stringLength_b >> WORD_SIZE_b);
    setWord(stream, bitIndex, split);
    bitIndex += WORD_SIZE_b;
    //rightmost 32 bits
    split = (unsigned long)stringLength_b;
    setWord(stream, bitIndex, split);
    bitIndex += WORD_SIZE_b;
    //end: adding length field
    //start: hash computation
    H[0] = 0x6a09e667;
    H[1] = 0xbb67ae85;
    H[2] = 0x3c6ef372;
    H[3] = 0xa54ff53a;
    H[4] = 0x510e527f;
    H[5] = 0x9b05688c;
    H[6] = 0x1f83d9ab;
    H[7] = 0x5be0cd19;
    unsigned long long numberOfBlocks = bitIndex/(WORD_SIZE_b*16);     //512 bit blocks
    int i = 1;
    for (; i <= numberOfBlocks; ++i) {
        //compute Wi
        unsigned long W[64];
        int j = 0;
        for (; j < 16; ++j) {
            W[j] = stream[(i - 1) * 16 + j];
            //todo: improve permutation box process
            //permutation box
            unsigned long old = W[j];
            int k = 0;
            for (; k < WORD_SIZE_b; ++k) {
                if (k/BYTE_SIZE!=1){    //any byte other than C byte
                    if(testLongBit(&old, WORD_SIZE_b-1-k))
                        setLongBit(&W[j], k);
                    else
                        clearLongBit(&W[j], k);
                }
                else{
                    if(testLongBit(&old, BYTE_SIZE + k))
                        setLongBit(&W[j], k);
                    else
                        clearLongBit(&W[j], k);
                }
            }
        }
        j = 16;
        for (; j < 64; ++j) {
            //compute sigma 0
            unsigned long shf12 = W[j-12] >> 12;
            unsigned long rot14 = (shf12 >> 2) | (W[j-12] << (WORD_SIZE_b - 14));
            unsigned long rot17 = (rot14 >> 3) | (rot14 << (WORD_SIZE_b - 3));
            unsigned long sigma0 = rot17 ^ rot14 ^ shf12;
            //compute sigma 1
            unsigned long shf9 = W[j-1] >> 9;
            unsigned long rot9 = shf9 | (W[j-1] << (WORD_SIZE_b - 9));
            unsigned long rot19 = (rot9 >> 10) | (rot9 << (WORD_SIZE_b - 10));
            unsigned long sigma1 = rot9 ^ rot19 ^ shf9;

//            printf("********************************\n");
//            if (j<24) {
//                printf("%d \n", j);
//                printf("SIG0: <%08lx> \n", sigma0);
//                printf("SIG1: <%08lx> \n", sigma1);
//                printf("W-6: <%08lx> \n", W[j-6]);
//                printf("W-15: <%08lx> \n", W[j-15]);
//                printf("//////////////////////////////////\n");
//            }
//            printf("********************************\n");

            unsigned long old = sigma1 + W[j-6] + sigma0 + W[j-15];

            //todo: improve permutation box process
            //permutation box
            int k = 0;
            for (; k < WORD_SIZE_b; ++k) {
                if (k/BYTE_SIZE!=1){    //any byte other than C byte
                    if(testLongBit(&old, WORD_SIZE_b-1-k))
                        setLongBit(&W[j], k);
                    else
                        clearLongBit(&W[j], k);
                }
                else{
                    if(testLongBit(&old, BYTE_SIZE + k))
                        setLongBit(&W[j], k);
                    else
                        clearLongBit(&W[j], k);
                }
            }

//            if (j<24) {
//                printf("%d \n", j);
//                printf("old: <%08lx> \n", old);
//                printf("new: <%08lx> \n", W[j]);
//            }
        }
//        printf("********************************\n");
//        for (int jj=16; jj < 24; ++jj) {
//            printf("<%08lx> ", W[jj]);
//        }
//        printf("********************************\n");
        //a through h
        unsigned long alphabet[8];
        j = 0;
        for (; j < 8; ++j) {
            alphabet[j] = H[j];
        }
//        printf("************ALPHABET************\n");
//        for (int jj=0; jj < 8; ++jj) {
//            printf("<%08lx> ", alphabet[jj]);
//        }
//        printf("********************************\n");
        //64 round loop
        j = 0;
        for (; j < 64; ++j) {
            unsigned long T1, T2, sigma0, sigma1, sigma2, ch, maj;
            //compute sigma0(a)
            unsigned long shf7 = alphabet[0] >> 7;
            unsigned long rot2 = alphabet[0] >> 2 | (alphabet[0] << (WORD_SIZE_b - 2));
            unsigned long rot13 = rot2 >> 11 | (rot2 << (WORD_SIZE_b - 11));
            unsigned long rot22 = rot13 >> 9 | (rot13 << (WORD_SIZE_b - 9));
            sigma0 = rot2 ^ rot13 ^ rot22 ^ shf7;
            //compute sigma1(e)
            unsigned long rot6 = alphabet[4] >> 6 | (alphabet[4] << (WORD_SIZE_b - 6));
            unsigned long rot11 = rot6 >> 5 | (rot6 << (WORD_SIZE_b - 5));
            unsigned long rot25 = rot11 >> 14 | (rot11 << (WORD_SIZE_b - 14));
            sigma1 = rot6 ^ rot11 ^ rot25;
            //compute sigma2(c+d)
            unsigned long argument = alphabet[2] + alphabet[3];
            unsigned long shf5 = argument >> 5;
            unsigned long rot2_s2 = argument >> 2 | (argument << (WORD_SIZE_b - 2));
            unsigned long rot3 = rot2_s2 >> 1 | (rot2_s2 << (WORD_SIZE_b - 1));
            unsigned long rot15 = rot3 >> 12 | (rot3 << (WORD_SIZE_b - 12));
            sigma2 = rot2_s2 ^ rot3 ^ rot15 ^ shf5;
            //compute ch(e, f, g)
            ch = (alphabet[4] & alphabet[5]) ^ (~alphabet[5] & alphabet[6]) ^ (~alphabet[4] & alphabet[6]);
            //compute maj(a, b, c)
            maj = (alphabet[0] & alphabet[2]) ^ (alphabet[0] & alphabet[1]) ^ (alphabet[1] & alphabet[2]);
            //compute new alphabet
            T2 = alphabet[7] + sigma1 + ch + K[j] + W[j];
            T1 = sigma0 + maj + sigma2;
            alphabet[7] = alphabet[6];
            alphabet[5] = alphabet[4];
            alphabet[3] = alphabet[2];
            alphabet[1] = alphabet[0];
            alphabet[6] = alphabet[5];
            alphabet[4] = alphabet[3] + T1;
            alphabet[2] = alphabet[1];
            alphabet[0] = 3*T1 - T2;
//            printf("************ALPHABET************\n");
//            printf("%d \n", j);
//            for (int jj=0; jj < 8; ++jj) {
//                printf("<%08lx> ", alphabet[jj]);
//            }
//            printf("\nc+d= <%08lx> \n", alphabet[2] + alphabet[3]);
//            printf("T2= <%08lx> \n", T2);
//            printf("ch= <%08lx> \n", ch);
//            printf("********************************\n");
        }
//        printf("************ALPHABET************\n");
//        for (int jj=0; jj < 8; ++jj) {
//            printf("<%08lx> ", alphabet[jj]);
//        }
//        printf("********************************\n");
        //compute new H
        j = 0;
        for (; j < 8; ++j) {
            H[j] += alphabet[j];
        }
    }
    //end: hash computation
}

void setStreamBit(unsigned long *A, int k)
{
    int i = k/WORD_SIZE_b;        //gives the corresponding index in the array A
    int pos = k%WORD_SIZE_b;      //gives the corresponding bit position in A[i]

    unsigned long flag = ~(~0ul >> 1);   // flag = 10000000000000000000000000000000

    flag = flag >> pos;      // flag = 0000...010...000   (shifted k positions)

    A[i] = A[i] | flag;      // Set the bit at the k-th position in A[i]
}

void clearStreamBit(unsigned long *A, int index)
{
    A[index/WORD_SIZE_b] &= ~( (~(~0ul >> 1)) >> (index%WORD_SIZE_b) );
}

int testStreamBit(unsigned long *A, int k)
{
    return ( (A[k/WORD_SIZE_b] & ( (~(~0ul >> 1)) >> (k%WORD_SIZE_b) ) ) != 0 ) ;
}

int testLongBit(unsigned long *A, int index)
{
    return ( (*A & ( (~(~0ul >> 1)) >> (index) ) ) != 0 ) ;
}

void setLongBit(unsigned long *A, int index)
{
    int pos = index;      //gives the corresponding bit position in A[i]

    unsigned long flag = ~(~0ul >> 1);   // flag = 10000000000000000000000000000000

    flag = flag >> pos;      // flag = 0000...010...000   (shifted k positions)

    *A = *A | flag;      // Set the bit at the k-th position in A[i]
}

void clearLongBit(unsigned long *A, int index)
{
    *A &= ~( (~(~0ul >> 1)) >> (index) );
}

void setByte(unsigned long *A,  int byteIndex, char byte )
{
    //todo: check byteIndex to be valid
    unsigned long l_byte = (unsigned long)byte;
    int index = byteIndex / WORD_SIZE_B;        //gives the corresponding index in the array A
    int section = byteIndex % WORD_SIZE_B;      //gives the corresponding section position in A[i]
    l_byte <<= (WORD_SIZE_b-BYTE_SIZE - section*BYTE_SIZE);

    A[index] = A[index] | l_byte;
}

void setWord(unsigned long *A, long long bitIndex, unsigned long word)
{
    //todo: check bitIndex to be valid
    A[bitIndex/WORD_SIZE_b] = word;
}

unsigned long long setString( unsigned long *A,  long long length, char *string )
{
    //todo: check offsetIndex to be valid
    long long offset = 0ll;
    while (offset != length)
    {
        unsigned long l_byte = (unsigned long)*string;
        long long index = offset / WORD_SIZE_B;        //gives the corresponding index in the array A
        long long section = offset % WORD_SIZE_B;      //gives the corresponding section position in A[i]
        l_byte <<= (WORD_SIZE_b-BYTE_SIZE - section*BYTE_SIZE);

        A[index] = A[index] | l_byte;

        ++offset;
        ++string;
    }
    return offset;
}