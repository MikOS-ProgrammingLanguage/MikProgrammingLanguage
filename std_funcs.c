#include <stdio.h>


int strlen(char* src){
	int i = 0;
	while (*src++)
		i++;
	return i;
}

char* strcpy(char* dest, const char* src) {
    do {
        *dest++ = *src++;
    } while (*src != 0);
    return 0;
}

int main()
{
    char* a = "Hello ";
    char* b = "World";
    strcnct(&a, &b);
    printf("%s", a);
}