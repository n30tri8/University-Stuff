#include <stdio.h>      /* printf, scanf, NULL */
#include <stdlib.h>     /* calloc, exit, free */
#include <string.h>     /* strlen, strcpy */
#include <stdint.h>     /* uint32_t, uint64_t */
#include <limits.h>     /* CHAR_BIT */


//RotateRight macro (only for procs with the 'ror' instruction)
#define RIGHTROTATE(in, bits) ({ uint32_t out; __asm__ __volatile__ ("\
    mov %1, %%eax;\n \
    ror %2, %%eax;\n \
    mov %%eax, %0;\n"\
    : "=r"(out) \
    : "r"(in), "c"((uint8_t)bits) \
    : "eax"); out;})

//Should be pretty portable
//#define RIGHTROTATE(x, n) (((int)((unsigned)x >> n)) | (x << (32 - n)))


typedef unsigned int uint;


uint32_t swap_uint32( uint32_t val )
{
    val = ((val << 8) & 0xFF00FF00 ) | ((val >> 8) & 0xFF00FF );
    return (val << 16) | (val >> 16);
}

/*
void p(int s,void* p){int i,j;for(i=s-1;i>=0;i--)for(j=7;j>=0;j--)printf("%u",(*((unsigned char*)p+i)&(1<<j))>>j);puts("");}


void dump512(uint32_t* buffer)
{
    for(uint i = 0; i < 512/32; i++)
    {
        p(sizeof(buffer[i]), &(buffer[i]));

        printf("\t %x \t", buffer[i]);

        char* temp = &buffer[i];

        for(uint j = 0; j < 4; j++)
        {
            printf("%c", temp[j]);
        }

        printf("\n");

        temp = NULL;
    }
}
*/


int main()
{
    //Set this to your input string
    char* input = "\x61\x62\x63";


    printf("\n\nRunning SHA256 hash function on: '%s'\n\n", input);


    //**********************|---bytes---|**|--bits--|
    uint64_t origInputLen = strlen(input) * CHAR_BIT;

    /*
    Note 1: All variables are 32 bit unsigned integers and addition is calculated modulo 232
    Note 2: For each round, there is one round constant k[i] and one entry in the message schedule array w[i], 0 ≤ i ≤ 63 (where i is between 0 and 63)
    Note 3: The compression function uses 8 working variables, a through h
    Note 4: Big-endian convention is used when expressing the constants in this pseudocode,
        and when parsing message block data from bytes to words, for example,
        the first word of the input message "abc" after padding is 0x80636261
    */

    //## Step 1
    //## Initialization
    //##

    //# Step 1a
    //## Initialize hash values
    //#

    // (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19):
    uint32_t h0 = 0x6a09e667;
    uint32_t h1 = 0xbb67ae85;
    uint32_t h2 = 0x3c6ef372;
    uint32_t h3 = 0xa54ff53a;
    uint32_t h4 = 0x510e527f;
    uint32_t h5 = 0x9b05688c;
    uint32_t h6 = 0x1f83d9ab;
    uint32_t h7 = 0x5be0cd19;


    //# Step 1b
    //## Initialize array of round constants
    //#

    // (first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311):
    const uint32_t k[64] = {
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    };


    //## Step 2
    //## Pre-processing
    //##

    uint numBlocks = 1 + ((origInputLen + 16 + 64) / 512); //Round up num blocks needed

    // Lets make a workable array
    uint32_t* paddedInput = calloc((512 / 32) * numBlocks, 32); // ((16) * num blocks, 32) (512 * num blocks [bits])


    /*
    printf("\n\n Should be empty\n");

    dump512(paddedInput);
    */


    memcpy(paddedInput, input, strlen(input));


    /*
    printf("\n\n Copied input\n");

    dump512(paddedInput);
    */


    // append the bit '1' to the message
    ((char*)paddedInput)[strlen(input)] = 0x80; //One in big-endian


    /*
    printf("\n\n Added one\n");

    dump512(paddedInput);
    */


    //Swap endianess from little to big-endian
    for(uint i = 0; i < (numBlocks * 16) - 1; i++)
    {
        paddedInput[i] = swap_uint32(paddedInput[i]);
    }

    paddedInput[((numBlocks * 512 - 64) / 32) + 1] = origInputLen;


    //## Step 3
    //## Process the message in successive 512-bit chunks
    //##

    //# Step 3a
    //## break message into 512-bit chunks
    //#

    //man printf("\t\t a \t\t b \t\t c \t\t d \t\t e \t\t f \t\t g \t\t h \n");


    for(uint i = 0; i < numBlocks; i++)
    {
        //# Setp 3b
        //## create a 64-entry message schedule array w[0..63] of 32-bit words
        //## (The initial values in w[0..63] don't matter, so many implementations zero them here)
        //#

        uint32_t* w = calloc(64, 32);

        //# Step 3c
        //## copy chunk into first 16 words w[0..15] of the message schedule array
        //#

        memcpy(w, &paddedInput[i * 16], 16 * 32); //Copy data from the correct block

        //# Step 3d
        //## Extend the first 16 words into the remaining 48 words w[16..63] of the message schedule array
        //#

        for(uint j = 16; j < 64; j++)
        {
            uint32_t s0   = RIGHTROTATE(w[j-15], 7) ^ RIGHTROTATE(w[j-15], 18) ^ (w[j-15] >> 3);
            uint32_t s1   = RIGHTROTATE(w[j-2], 17) ^ RIGHTROTATE(w[j-2], 19) ^ (w[j-2] >> 10);

            w[j] = w[j-16] + s0 + w[j-7] + s1;
        }

        //## Step 5
        //## Compression
        //##

        //# Setp 5a
        //## Initialize working variables to current hash value
        //#

        uint32_t a = h0;
        uint32_t b = h1;
        uint32_t c = h2;
        uint32_t d = h3;
        uint32_t e = h4;
        uint32_t f = h5;
        uint32_t g = h6;
        uint32_t h = h7;


        //man printf("init: \t\t %x \t %x \t %x \t %x \t %x \t %x \t %x \t %x \n", a, b, c, d, e, f, g, h);

        //# Step 5b
        //## Compression function main loop
        //#

        for(uint j = 0; j < 64; j++)
        {
            uint32_t S1 = RIGHTROTATE(e, 6) ^ RIGHTROTATE(e, 11) ^ RIGHTROTATE(e, 25);
            uint32_t ch = (e & f) ^ ((~e) & g);

            uint32_t temp1 = h + S1 + ch + k[j] + w[j];

            uint32_t S0 = RIGHTROTATE(a, 2) ^ RIGHTROTATE(a, 13) ^ RIGHTROTATE(a, 22);
            uint32_t maj = (a & b) ^ (a & c) ^ (b & c);

            uint32_t temp2 = S0 + maj;
//            if(j==0){
//                printf("h:<%08lx>\ts1:<%08lx>\tch:<%08lx>\tk[0]:<%08lx>\tw[0]:<%08lx>\t \n", h , S1 , ch , k[j] , w[j]);
//            }
            h = g;
            g = f;
            f = e;
            e = d + temp1;
            d = c;
            c = b;
            b = a;
            a = temp1 + temp2;


            //man printf("comp =  %i \t %08x \t %08x \t %08x \t %08x \t %08x \t %08x \t %08x \t %08x \n", j, a, b, c, d, e, f, g, h);

        }
//        printf("%d: <%8lx> \n", 0, a);
//        printf("%d: <%8lx> \n", 1, b);
//        printf("%d: <%8lx> \n", 2, c);
//        printf("%d: <%8lx> \n", 3, d);
//        printf("%d: <%8lx> \n", 4, e);
//        printf("%d: <%8lx> \n", 5, f);
//        printf("%d: <%8lx> \n", 6, g);
//        printf("%d: <%8lx> \n", 7, h);


        //## Step 6
        //## Add the compressed chunk to the current hash value
        //##

        printf("h    =  %i \t %08x \t %08x \t %08x \t %08x \t %08x \t %08x \t %08x \t %08x \n",
                   i, a, b, c, d, e, f, g, h);


        h0 += a;
        h1 += b;
        h2 += c;
        h3 += d;
        h4 += e;
        h5 += f;
        h6 += g;
        h7 += h;

        free(w);
    }


    //## Step 7
    //## Produce the final hash value (big-endian)
    //##

    uint32_t digest[8] = { h0, h1, h2, h3, h4, h5, h6, h7 };

    free(paddedInput);


    printf("\n\nDigest: %x%x%x%x%x%x%x%x\n", digest[0], digest[1], digest[2], digest[3], digest[4], digest[5], digest[6], digest[7]);


    return 0;
}
