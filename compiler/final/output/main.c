#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>

#include "stack.h"

double n1;
double n2;
double n3;
double root_scp0_kjj0;
double root_scp0_kjj1;
double root_scp0_kjj2;
double root_scp0_kjj3;
double root_scp0_kjj4;
double root_scp0_kjj5;
double root_scp0_kjj6;
double root_scp0_scp1_scp2_kjj0;
double root_scp0_scp1_scp2_kjj1;

int main(){
	struct stack *main_stack;

	main_stack = stack_create();
	L0: n1 = 0;
	L1: n2 = 0;
	L2: n3 = 0;
	L3: root_scp0_kjj0 = 10 / 2;
	L4: root_scp0_kjj1 = 20 - root_scp0_kjj0;
	L5: n1 = root_scp0_kjj1;
	L6: root_scp0_kjj2 = 3 + 2;
	L7: root_scp0_kjj3 = n1 / root_scp0_kjj2;
	L8: n2 = root_scp0_kjj3;
	L9: root_scp0_kjj4 = n1 * n2;
	L10: root_scp0_kjj5 = root_scp0_kjj4 - 10;
	L11: n3 = root_scp0_kjj5;
	L12: if (n1 > 2)
	L13: goto L15;
	L14: goto L26;
	L15: n2 = 3;
	L16: if (n2 < 0)
	L17: goto L25;
	L18: goto L19;
	L19: root_scp0_scp1_scp2_kjj0 = n3 + 2;
	L20: n3 = root_scp0_scp1_scp2_kjj0;
	L21: root_scp0_scp1_scp2_kjj1 = n2 - 1;
	L22: n2 = root_scp0_scp1_scp2_kjj1;
	L23: None = n2 - 1;
	L24: goto L16;
	L25: goto L31;
	L26: if (n2 != 3)
	L27: goto L29;
	L28: goto L31;
	L29: n2 = 80;
	L30: goto L31;
	L31: root_scp0_kjj6 = n3 + 1;
	L32: n3 = root_scp0_kjj6;
	L33:;
}