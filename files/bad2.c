#include <stdio.h>
#include <stdlib.h>
#define N 1000005
int a[N], b[N];
int compare(const void *a, const void *b)
{
    return (*(int *)b - *(int *)a);
}
int main()
{
    int n, y = 1, i, j;
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);
    qsort(a, n, sizeof(int), compare);
    b[0] = a[0];
    for (i = 1; i < n; i++)
    {
        for (j = 0; j < y; j++)
            if (b[j] % a[i] == 0)
                break;
        if (j == y)
            b[y++] = a[i];
    }
    printf("%d\n", y);
    for (i = 0; i < y; i++)
        printf("%d ", b[i]);
}