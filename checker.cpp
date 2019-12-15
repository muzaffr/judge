#include <bits/stdc++.h>
using namespace std;

const int N = 1e6 + 5;

int main()
{
    int n;
    cin >> n;
    vector<int> vi(n), vo;
    for(int i = 0; i < n; ++i)
        cin >> vi[i];
    
    set<int> s, t;
    if(n > 1)
        s.insert(1);
    for(int it : vi)
        for(int i = 2; i*i <= it; ++i)
            if(it % i == 0)
                s.insert(i), s.insert(it/i);

    for(int it : vi)
        if(not s.count(it))
            t.insert(it);
    int mi = t.size();

    string sin;
    if(not(cin >> sin))
        return cout << "unexpected EOF", 2;
    int mo;
    try
    {
        mo = stoi(sin);
    }
    catch(...)
    {
        return cout << "expected int32", 2;
    }

    if(mi != mo)
        return cout << "wrong answer", 2;

    for(int i = 0; i < mo and cin >> sin; ++i)
    {
        try
        {
            vo.push_back(stoi(sin));
        }
        catch(...)
        {
            return cout << "expected int32", 2;
        }
    }
    if(cin >> sin)
        return cout << "expected EOF", 2;
    if(vo.size() != mo)
        return cout << "unexpected EOF", 2;


    set<int> u(vo.begin(), vo.end());
    if(t == u)
        return cout << "ok", 1;
    return cout << "wrong answer", 2;
}