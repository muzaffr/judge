#include <stdio.h>
#define N 100000
int a[N], f[N];
int main()
{
    int n;
    scanf("%d", &n);
    f[1] = n != 1;
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &a[i]);
        for (int j = 2; j * j <= a[i]; j++)
            if (a[i] % j == 0)
                f[j] = f[a[i] / j] = 1;
    }
    int c = 0;
    for (int i = 0; i < n; i++)
        if (!f[a[i]])
            c++;
    printf("%d\n", c);
    for (int i = 0; i < n; i++)
        if (!f[a[i]])
            printf("%d ", a[i]);
}