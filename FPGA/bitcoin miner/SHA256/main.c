#include <stdio.h>

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
int testBit(unsigned long *A,  int k );
void setBit(unsigned long *A,  int k );
void clearBit(unsigned long *A,  int k );
void setWord(unsigned long *A, long long bitIndex, unsigned long word);
unsigned long long setString( unsigned long *A,  long long offsetIndex, char *string );
void SHA256(unsigned long *stream, unsigned long long stringLength, unsigned long *H);

int main() {
    //todo: check assumption
    // ulong type is 4B, long long type is 8B
    // blockHeader length is less than 512+447 bits
    //unsigned char *blockHeader = "\x65";
    unsigned char *blockHeader = "abcd";

    unsigned long stream[MAX_LENGTH];
    for (int i = 0; i < MAX_LENGTH; ++i) {
        stream[i] = 0ul;
    }

    unsigned long long streamLength = setString(stream, 0ll, blockHeader);

    unsigned long hash[MAX_LENGTH];
    SHA256(stream, streamLength, hash);


}

void SHA256(unsigned long *stream, unsigned long long stringLength, unsigned long *H) {
    unsigned long long bitIndex = stringLength*BYTE_SIZE;
    setBit(stream, bitIndex);
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
        clearBit(stream, bitIndex);
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
        clearBit(stream, bitIndex);
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
    for (int i = 1; i <= numberOfBlocks; ++i) {
        //compute Wi
        unsigned long W[64];
        for (int j = 0; j < 16; ++j) {
            W[j] = stream[(i - 1) * 16 + j];
        }
        for (int j = 16; j < 64; ++j) {
            //compute sigma 0
            unsigned long shf3 = W[j-15] >> 3;
            unsigned long rot7 = (shf3 >> 4) | (W[j-15] << (WORD_SIZE_b - 7));
            unsigned long rot18 = (rot7 >> 11) | (rot7 << (WORD_SIZE_b - 11));
            unsigned long sigma0 = rot7 ^ rot18 ^ shf3;
            //compute sigma 1
            unsigned long shf10 = W[j-2] >> 10;
            unsigned long rot17 = (shf10 >> 7) | (W[j-2] << (WORD_SIZE_b - 17));
            unsigned long rot19 = (rot17 >> 2) | (rot17 << (WORD_SIZE_b - 2));
            unsigned long sigma1 = rot17 ^ rot19 ^ shf10;

            W[j] = sigma1 + W[j-7] + sigma0 + W[j-16];
        }
//        for (int j = 0; j < 64; ++j) {
//            if (j%11 == 0 && j !=0)
//                printf("\n");
//            printf("<%8lx> ", W[j]);
//        }
//        printf("\n");
        //a through h
        unsigned long alphabet[8];
        for (int j = 0; j < 8; ++j) {
            alphabet[j] = H[j];
        }
        //64 round loop
        for (int j = 0; j < 64; ++j) {
            unsigned long T1, T2, sigma0, sigma1, ch, maj;
            //compute sigma0(a)
            unsigned long rot2 = alphabet[0] >> 2 | (alphabet[0] << (WORD_SIZE_b - 2));
            unsigned long rot13 = rot2 >> 11 | (rot2 << (WORD_SIZE_b - 11));
            unsigned long rot22 = rot13 >> 9 | (rot13 << (WORD_SIZE_b - 9));
            sigma0 = rot2 ^ rot13 ^ rot22;
            //compute sigma1(e)
            unsigned long rot6 = alphabet[4] >> 6 | (alphabet[4] << (WORD_SIZE_b - 6));
            unsigned long rot11 = rot6 >> 5 | (rot6 << (WORD_SIZE_b - 5));
            unsigned long rot25 = rot11 >> 14 | (rot11 << (WORD_SIZE_b - 14));
            sigma1 = rot6 ^ rot11 ^ rot25;
            //compute ch
            ch = (alphabet[4] & alphabet[5]) ^ (~alphabet[4] & alphabet[6]);
            //compute maj
            maj = (alphabet[0] & alphabet[1]) ^ (alphabet[0] & alphabet[2]) ^ (alphabet[1] & alphabet[2]);
            //compute new alphabet
            T1 = alphabet[7] + sigma1 + ch + K[j] + W[j];
            T2 = sigma0 + maj;
//            if(j==0){
//                printf("h:<%08lx>\ts1:<%08lx>\tch:<%08lx>\tk[0]:<%08lx>\tw[0]:<%08lx>\t \n", alphabet[7] , sigma1 , ch , K[j] , W[j]);
//            }
//            if(j==0){
//                printf("T1:<%08lx>\tT2:<%08lx> \n", T1, T2);
//            }
            alphabet[7] = alphabet[6];
            alphabet[6] = alphabet[5];
            alphabet[5] = alphabet[4];
            alphabet[4] = alphabet[3] + T1;
            alphabet[3] = alphabet[2];
            alphabet[2] = alphabet[1];
            alphabet[1] = alphabet[0];
            alphabet[0] = T1 + T2;
        }
//        for (int j = 0; j < 8; ++j) {
//            printf("%d: <%8lx> \n", j, alphabet[j]);
//        }
        //compute new H
        for (int j = 0; j < 8; ++j) {
            H[j] += alphabet[j];
        }
    }
    //end: hash computation
//    for (int i = 0; i < 512; ++i) {
//        if(i != 0) {
//            if (i % 8 == 0) {
//                printf("   ");
//            }
//            if (i % 64 == 0) {
//                printf("\n");
//            }
//        }
//        printf("%d", testBit(stream, i));
//    }

    for (int i = 0; i < 8; ++i) {
        printf("<%08lx> ", H[i]);
    }


}

void setBit(unsigned long *A,  int k )
{
    int i = k/WORD_SIZE_b;        //gives the corresponding index in the array A
    int pos = k%WORD_SIZE_b;      //gives the corresponding bit position in A[i]

    unsigned long flag = ~(~0ul >> 1);   // flag = 10000000000000000000000000000000

    flag = flag >> pos;      // flag = 0000...010...000   (shifted k positions)

    A[i] = A[i] | flag;      // Set the bit at the k-th position in A[i]
}

void clearBit(unsigned long *A,  int k )
{
    A[k/WORD_SIZE_b] &= ~( (~(~0ul >> 1)) >> (k%WORD_SIZE_b) );
}

int testBit(unsigned long *A,  int k )
{
    return ( (A[k/WORD_SIZE_b] & ( (~(~0ul >> 1)) >> (k%WORD_SIZE_b) ) ) != 0 ) ;
}

void setWord(unsigned long *A, long long bitIndex, unsigned long word)
{
    //todo: check bitIndex to be valid
    A[bitIndex/WORD_SIZE_b] = word;
}

unsigned long long setString( unsigned long *A,  long long offsetIndex, char *string )
{
    //todo: check offsetIndex to be valid
    while (*string)
    {
        unsigned long l_byte = (unsigned long)*string;
        long long index = offsetIndex / WORD_SIZE_B;        //gives the corresponding index in the array A
        long long section = offsetIndex % WORD_SIZE_B;      //gives the corresponding section position in A[i]
        l_byte <<= (WORD_SIZE_b-BYTE_SIZE - section*BYTE_SIZE);

        A[index] = A[index] | l_byte;

        ++offsetIndex;
        ++string;
    }


    return offsetIndex;
}