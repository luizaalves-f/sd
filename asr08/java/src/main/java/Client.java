import com.zeroc.Ice.Communicator;

import Demo.PrinterPrx;

public class Client {

    public static void main(String[] args) {

        if (args.length < 1) {
            System.out.println(
                "Uso: java Client <IP_DO_SERVIDOR>"
            );
            return;
        }

        String host = args[0];

        try (Communicator communicator = new Communicator(args)) {

            PrinterPrx printer = PrinterPrx.createProxy(
                communicator,
                "SimplePrinter:tcp -h " + host + " -p 5678"
            );

            String rep = printer.printString(
                "Hello from Java client!"
            );
            System.out.println(
                "Resposta printString: " + rep
            );

            rep = printer.inverterString(
                "Sistemas Distribuidos"
            );
            System.out.println(
                "String invertida: " + rep
            );

            int quantidade = printer.contarCaracteres(
                "Sistemas Distribuidos"
            );
            System.out.println(
                "Quantidade de caracteres: " + quantidade
            );
        }
    }
}