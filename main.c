
//#include <math.h>

//#define forever for(;;);  //无限循环
//
//#define max(A, B) ((A)> (B) ? (A): (B))
//int x = max(p+q, r+s);
////x = ((p+q) > (r+s) ? (p+q) : (r+s));
//
//
//double try(double i){
//    forever;
//    return i;
//}
//
//#if !defined(HDR)
//#define HDR
///* hdr.h 的内容放在这里 */
//#endif
//

//#if SYSTEM == SYSV
//#define HDR "sysv.h"
//#elif SYSTEM == BSD
//#define HDR "bsd.h"
//#elif SYSTEM == MSDOS
//#define HDR "msdos.h"
//#else
//#define HDR "default.h"
//#endif
//#include HDR
//
//
//#ifndef HDR
//#define HDR
///* hdr.h 的内容放在这里 */
//#endif
//
//#define MAX 100
//
//int num[MAX];

//#define VTAB '\013' /* ASCII 纵向制表符 */
//#define BELL '\007' /* ASCII 响铃符 */
//
////常量表达式是其中只包含常量的表达式。这种表达式的求值可以在编译时完成，而不必等
////到运行时才进行，因而它可用于常量能够出现的任何位置。例如：
//#define MAXLINE 1000
//char line[MAXLINE+1];
//
//#define LEAP 1 /* 闰年 */
//int days[31+28+LEAP+31+30+31+30+31+31+30+31+30+31];
//
////字符串常量也叫 字符串字面值，是用双引号括上的由零个到多个字符组成的序列。例如:
//char a[] = "I am a string";
////或：
//char b[] = ""; /* 空字符串 */
//
//enum escapes { BELL = '\a', BACKSPACE = '\b', TAB = '\t',
//    NEWLINE = '\n', VTAB = '\v', RETURN = '\r' };
//enum moths { JAN = 1, FEB , MAR, APR, MAY, JUN,
//    JUL, AUG, SEP, OCT, NOV, DEC };
///* FEB 为 2，MAR 为 3，依次类推 */
//enum try {A=12, B = 3, c, d, e};


//struct point {
//    int x;
//    int y;
//};
//struct rect {
//    struct point pt1;
//    struct point pt2;
//};
// struct key {
//        char *word;
//        int count;
//    } keytb[] = {
//            "auto", 0,
//            "break", 0,
//            "case", 0,
//            "char", 0,
//            "const", 0,
//            "continue", 0,
//            "default", 0,
//            "unsigned", 0,
//            "void", 0,
//            "volatile", 0,
//            "while", 0
//    };
//    printf("%d", sizeof keytb);
//     typedef struct tnode *Treepstr;
////   typedef struct tnode {
////       char *word;
////       int count;
////       Treepstr left;
////       Treepstr right;
////   }Treenode;
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void try_static();
int astrcmp(char*, char*);
int pstrcmp(char*, char*);
void astrcopy(char[], char[]);
void pstrcopy(char*, char*);
void writelines(char *[], int);
char *month_name(int);

struct point make_point(int, int);
struct point point_add(struct point, struct point);

int main(int argc, char *argv[]) {
    union union_tag {
        int i_val;
        float f_val;
        double d_val;
    }union_tag1;
    return 0;
}

 struct point point_add(struct point p1, struct point p2){
    p1.x += p2.x;
    p1.y += p2.y;
    return p1;
}

struct point make_point(int x, int y){
    struct point temp;
    temp.x = x;
    temp.y = y;
    return temp;
}

char *month_name(int n){
    static char* name[] = {
            "Illegal month", "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
    };
    return n < 1 || n > 12 ? *name : *(name + n);
}



void writelines(char *lineptr[], int nlines){
    while (nlines-- > 0)
        printf("%s\n", *lineptr++);
}


//第一个函数是 strcpy(s,t)，其将字符串 t 复制到字符串 s 中。
//用 s = t 来表达当 然很好，但这样复制的不是字符串而是指针。为了复制字符串，我们需要一个循环。
//数组版本：
void astrcopy(char s[], char t[]){
    int i = 0;
    while (t[i] = s[i])
        i++;
}
//指针版本
//*t++的值为t增加之前所指向的字符；后缀 ++ 在 字符被获取之后才改变 t。
//同样地，该字符被存放到原 s 的位置后 s 才被递增。
//该字符还作为 与‘\0’相比较的值来控制循环。
//其最终效果就是字符从 t 复制到 s，直到包含结尾的‘\0’为止。
void pstrcopy(char *s, char *t){
    while(*t++ = *s++)
        ;
}

int astrcmp(char* s, char* t){
    int i;
    for (i = 0; s[i] == t[i]; i++) // 精妙手法
        if (s[i] == '\0')
            return 0;
    return s[i] - t[i];
}

int pstrcmp(char* s, char* t){
    for (; *s == *t ; s++, t++)
        if (*s == '\0')
            return 0;
    return *s - *t;
}

struct tnode talloc(void){
    return (struct tnode *)malloc(sizeof(struct tnode));
}
//void * 到 ALMOSTANYTYPE * 的转换是自动的，因此这种强制转换并 不必要；
//而且如果 malloc 或其替代者未声明为返回 void *，显式的强制转换还会掩盖这一不经意的错误。
//另一 方面，在 ANSI 标准之前，这种强制转换则是必须的。

char *strdup(char *s){
    void pstrcopy(char*, char*);
    char *p;
    p = (char *)malloc(strlen(s));
    if (p != NULL)
        pstrcopy(s, p);
    return p;
}

//char a[] = "he";
//char b[] = "wo";
//pstrcopy(a, b);
//printf("%s\n", b);
//printf("%d\n", sizeof(a));
//printf("%c", *(a + 1));
//return 0;

//    int n = 3;
//    int m = 3;
//    int flag;
//    scanf("%d", &flag);
//    int a = flag ? ++n: ++m;
//
//    printf("%d, %d, %d", n, m, a);
//    static int i;
//    int s[10] = {};
//    if (n >= 0)
//        for (i = 0; i < n; i++)
//            if (s[i] > 0) {
//                printf("...");
//                return i;
//            }
//            else /* 错了！*/
//                printf("错误 -- n 是一个负数\n");

//    char a[] = "xyz";
//    char b[] = {'x','y','z'};
//    printf("%d, %d\n", sizeof(a), sizeof(b)); //4, 3
    //    try_static();
//    try_static();
//    try_static();

//    int i = 10;
//    for (i = 0; i < 13; ++i) {
//        int i;
//        i = 19;
//    }
//    printf("%d", i); //13\
//  cha

//    int a[10];
//    int b[5];
//    int c[3];
//    printf("%p,%p\n", a, b);
//    printf("%d\n", a > c);
//    printf("%p\n", b + 10);
//    printf("%d\n", *(c + 5));

//printf("hello"", world"); //hello world
//printf("%d, %d, %d, %d", A, B, c, d);
//    extern int max;
//    const double e = 2.71828;
//    e = 1;
//    long a = 10000000;
//    printf("%ld", a);
//    printf("%d", '\0');
//    double nc;
//    for (nc = 0; getchar() != '0' ; nc++)
//        ;
//    printf("%.0f\n", nc);

//    printf("%c", 65); //A


//char *strline[] = {
//        "hello",
//        "world",
//        "C is cool",
//        "Python is awesome too"
//};
//writelines(strline, 3);

void try_static(){
    static int i = 1;
    printf("%d", i++);
}




