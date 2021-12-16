Function Int fibonacci(Int n) Open
	If(n < 2) Open
		Back n;
	Close
	Else Open
		Back fibonacci(n - 1) + fibonacci(n - 2);
	Close
Close

Function Int Main ( ) Open
	Int n, total;
	Print('Insira o tamanho da sequencia:');
	Scan(n);

	For (Int i = 0, 1, n) Open
		total = fibonacci(i);
        Print(total);
	Close

	Back;
Close