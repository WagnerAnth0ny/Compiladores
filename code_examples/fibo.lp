Function Int fibonacci(Int n) Open
    If(n < 2) Open
        Back n;
    Close
    Else Open
        Back fibonacci(n - 1) + fibonacci(n - 2);
    Close
Close

Function Empty limitedfibonacci(Int x) Open
    Int i = 1, current;

    While (fibonacci(i) < x) Open
        current = fibonacci(i);
        Print(current);
        i = i + 1;
    Close

    Back;
Close

Function Int Main ( ) Open
    Int n, total;
    Print('Insira um valor limite: ');
    Scan(n);

    limitedfibonacci(n);

    Back 0;
Close
