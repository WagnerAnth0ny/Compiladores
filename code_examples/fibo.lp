Function Int fibonacci(Int n) Open
    If(n < 2) Open
        Back n;
    Close
    Else Open
        Back fibonacci(n - 1) + fibonacci(n - 2);
    Close
Close

Function Empty limited_fibonacci(Int x) Open
    i = 1
    While (fibonacci(i) < x) Open
        Print(fibonacci(i));
        i = i + 1;
    Close

    Back;
Close

Function Int Main ( ) Open
    Int n, total;
    Print('Insira um valor limite: ');
    Scan(n);

    limited_fibonacci(n);

    Back 0;
Close
