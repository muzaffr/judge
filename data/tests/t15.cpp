#include <iostream>
#include <vector>
using namespace std;
int main()
{
    ios::sync_with_stdio(0), cin.tie(0);
    int N = 1e3;
    vector<int> isprime(N + 5, 1);
    vector<int> primes;
    vector<int> SPF(N + 5);
    isprime[0] = isprime[1] = 0;
    for (int i = 2; i < N; i++)
    {
        if (isprime[i])
            primes.push_back(i), SPF[i] = i;
        for (int j = 0; j < primes.size() && i * primes[j] < N && primes[j] <= SPF[i]; j++)
            isprime[i * primes[j]] = 0, SPF[i * primes[j]] = primes[j];
    }
    vector<int> v;
    for (int i : primes)
    {
        long long x = i;
        while (x < 1000000)
            v.push_back(x), x *= i;
    }
    cout << v.size() << " \n";
    for (int i : v)
        cout << i << " ";
    cout << endl;
}