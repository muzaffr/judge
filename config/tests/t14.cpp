#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
using namespace std;
#define ll int64_t

// uniform_int_distribution<int> dist(1, 1000000);
const int N = 1e6;
mt19937 rng(528491);

int main()
{
    ios::sync_with_stdio(0), cin.tie(0);
    vector<int> v(N);
    iota(v.begin(), v.end(), 1);
    shuffle(v.begin(), v.end(), rng);
    cout << N / 10 << "\n";
    for (ll i = 0; i < N / 10; i++)
        cout << v[i] << " ";
    cout << endl;
    return 0;
}