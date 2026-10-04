import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.Current;
import com.zeroc.Ice.Identity;
import com.zeroc.Ice.ObjectAdapter;

import Demo.Printer;

public class Server {

    static class PrinterI implements Printer {

        @Override
        public String printString(String s, Current current) {
            System.out.println("printString: " + s);
            return s + "*";
        }

        @Override
        public String inverterString(String s, Current current) {
            String resultado = new StringBuilder(s).reverse().toString();
            System.out.println("inverterString: " + resultado);
            return resultado;
        }

        @Override
        public int contarCaracteres(String s, Current current) {
            int quantidade = s.length();
            System.out.println("contarCaracteres: " + quantidade);
            return quantidade;
        }
    }

    public static void main(String[] args) {

        try (Communicator communicator = new Communicator(args)) {

            ObjectAdapter adapter =
                communicator.createObjectAdapterWithEndpoints(
                    "SimpleAdapter",
                    "tcp -p 5678"
                );

            PrinterI printer = new PrinterI();

            adapter.add(
                printer,
                new Identity("SimplePrinter", "")
            );

            adapter.activate();

            System.out.println(
                "Servidor Java aguardando requisições na porta 5678..."
            );

            communicator.waitForShutdown();
        }
    }
}