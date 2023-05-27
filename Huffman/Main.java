package newpackage;

import java.io.*;

public class Main {

    public static void main(String[] args) throws IOException {
//        HuffmanCodes t = new HuffmanCodes();
//        if(args.length==0){
//            t.printGuide();
//            return;
//        }
//        if(args[0].equalsIgnoreCase("c")){
//            if(args.length!=3){
//                t.printGuide();
//                return;
//            }
//            long start = System.currentTimeMillis();
//            t.CompressFile(args[1],Integer.parseInt(args[2]));
//            long end = System.currentTimeMillis();
//            System.out.println("compressing took: "+( (end-start)/1000F )+ "sec");
//
//        }
//        else if(args[0].equalsIgnoreCase("d")){
//            if(args.length!=2){
//                t.printGuide();
//                return;
//            }
//            long start = System.currentTimeMillis();
//            t.DecompressingFile(args[1]);
//            long end = System.currentTimeMillis();
//            System.out.println("decompression took: "+( (end-start)/1000F )+ "sec");
//
//        }
//        else{
//            t.printGuide();
//        }

        HuffmanCodes t = new HuffmanCodes();
        String file_path = "./test100.txt";
        String zip_path = "./18011174.1.test100.txt.hc";
        int n_bytes = 1;

        long start = System.currentTimeMillis();
        t.CompressFile(file_path, n_bytes);
        long end = System.currentTimeMillis();
        System.out.println("compressing took: "+( (end-start)/1000F )+ "sec");

        start = System.currentTimeMillis();
        t.DecompressingFile(zip_path);
        end = System.currentTimeMillis();
        System.out.println("decompression took: "+( (end-start)/1000F )+ "sec");
    }
}