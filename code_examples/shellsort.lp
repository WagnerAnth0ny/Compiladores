Function Empty shellsort(Int array[5], Int n) Open
		Int c, j;
        Int h = 1;

        While (h < n) Open
			h = h * 3 + 1;
		Close

		h = h / 3;

		While(h > 0) Open

			For (Int i = h, 1, n) Open

                    c = array[i];
                    j = i;

                    While (j >= h And array[j - h] > c) Open

                            array[j] = array[j - h];
                            j = j - h;

                    Close

                    array[j] = c;
			Close

			h = h / 2;
        
		Close

		Back;

	Close

Function Int Main ( ) Open
		Int n, current;
		Print('Insira o tamanho do array: ');
		Scan(n);

		Int array[n];

		Print('Insira os elementos do array: ');

        For (Int i = 0, 1, n) Open
	        Scan(array[i]);
        Close

        Print('Valores adicionados: ');

        For (Int i = 0, 1, n) Open
            current = array[i];
	        Printnl(current);
        Close

		shellsort(array[n], n);

		Print('Valores ordenados: ');

        For (Int i = 0, 1, n) Open
            current = array[i];
	        Printnl(current);
        Close

		Back 0;
Close