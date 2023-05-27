package newpackage;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Stack;

public class HuffmanCodes {
    public Node ConstructHuffManTree(HashMap<String,Integer> statistics){
        PriorityQueue<Node> queue = new PriorityQueue<>();
        for (Map.Entry<String, Integer> entry : statistics.entrySet()) {
            int key = entry.getValue();
            String value = entry.getKey();
            //insert all values into the minHeap
            Node l = new Node(key,value);
            queue.add(l);
        }
        // extract the Least 2 values, add to the tree and combine there values as a new object
        while(queue.size()>1){
            Node c1 = queue.poll();
            Node c2 = queue.poll();
            Node t = new Node(c1,c2);
            queue.add(t);
        }
        return queue.poll();
    }
    public String encodeTree(Node root){
        StringBuilder encoded = encodeTreeRecursion(root , new StringBuilder());
        return encoded.toString();
    }
    public StringBuilder encodeTreeRecursion(Node node , StringBuilder s){
        if(node.isLeaf()){
            char l = (char)node.getValue().length();
            s.append(l);
            s.append(node.getValue());
            return s;
        }
        s.append("0");
        if(node.left != null)
            encodeTreeRecursion(node.left, s);
        if(node.right != null)
            encodeTreeRecursion(node.right, s);
        return s;
    }

    public Node constructHuffmanTree(StringBuilder encodedTree){
        Stack<Node> s = new Stack<>();
        Node root = new Node();
        s.add(root);
        Node node;
        while(!s.isEmpty()){
            node = s.pop();
            if(encodedTree.length()<=0)break;
            if (encodedTree.charAt(0)=='0'){
                encodedTree.deleteCharAt(0);
                node.left = new Node();
                node.right = new Node();
                s.add(node.right);
                s.add(node.left);
            }
            else{
                int codeLength = encodedTree.charAt(0);
                encodedTree.deleteCharAt(0);
                String v= encodedTree.subSequence(0,codeLength).toString();
                encodedTree.delete(0,codeLength);
                node.setVal(v);
            }
        }
        return root;
    }

    public HashMap<String,String> createDictionary(Node root){
        HashMap<String,String> dictionary = new HashMap<>();
        // base case where there is only 1 token in the given file
        if(root.isLeaf()){
            dictionary.put(root.getValue(),"0");
            return dictionary;
        }
        StringBuilder s = new StringBuilder();
        createDictionaryRecurse(dictionary,root,s);
        return dictionary;
    }

    public HashMap<String,String> createDictionaryRecurse(HashMap<String,String> dictionary,
                                                          Node node, StringBuilder representation){
        if(node.isLeaf()){
            dictionary.put(String.valueOf(node.getValue()), String.valueOf(representation));
            return dictionary;
        }
        if(node.left!=null){
            createDictionaryRecurse(dictionary, node.left,
                    new StringBuilder().append(representation).append("1"));
        }
        if(node.right!=null){
            createDictionaryRecurse(dictionary, node.right,
                    new StringBuilder().append(representation).append("0"));
        }
        return dictionary;
    }
    //
    public void ConvertAndWriteFile(HashMap<String,String> dictionary , String inputFilePath,
                                    int n, int lastByteNBits , String encodedTree, String outputFilePath){
        int bitPosition = 0;
        try(InputStream inputStream = new BufferedInputStream(new FileInputStream(inputFilePath));
            OutputStream outputStream = new BufferedOutputStream(new FileOutputStream(outputFilePath))){
            int byteRead;
            StringBuilder setOfBits = new StringBuilder(8);
            // last byte contains n bits
            outputStream.write(lastByteNBits);
            //add dictionary information
            for(int c : encodedTree.toCharArray()){
                outputStream.write(c);
            }
            // add a separator between the dictionary and the file
            outputStream.write('\n');

            while((byteRead = inputStream.read()) != -1) {
                // read n characters at a time
                StringBuilder s = new StringBuilder();
                s.append((char)byteRead);
                for (int i = 0; i < n-1; i++) {
                    if((byteRead = inputStream.read()) != -1){
                        s.append((char)byteRead);
                    }
                    else break;
                }
                // each 8 bits are compressed as 1 byte in the file
                String bitRepresentation = dictionary.get(s.toString());
                for (int i = 0; i < bitRepresentation.length(); i++) {
                    if(bitPosition==8){
                        outputStream.write(Integer.parseInt(setOfBits.toString(),2));
                        bitPosition=0;
                        setOfBits = new StringBuilder(8);
                    }
                    setOfBits.append(bitRepresentation.charAt(i));
                    bitPosition++;
                }
            }
            if(bitPosition>0){
                for (int i = bitPosition; i < 8; i++) {
                    setOfBits.append("0");
                }
                outputStream.write(Integer.parseInt(setOfBits.toString(),2));
            }
        }
        catch(IOException ex){
            System.out.println("IO Exception");
            return;
            //ex.printStackTrace();
        }
    }
    //
    public void CompressFile(String inputFilePath , int n){
        //
        File file = new File(inputFilePath);
        String outputFilePath = "18011174." + n + "." + file.getName() + ".hc";
        if(file.getParentFile()!=null){
            outputFilePath = file.getParentFile() + "\\" + outputFilePath;
        }
        HashMap<String,Integer> statistics = new HashMap<>();
        System.out.println("reading file....");
        try(InputStream inputStream = new BufferedInputStream(new FileInputStream(inputFilePath))){
            int byteRead;
            while((byteRead = inputStream.read()) != -1) {
                StringBuilder s = new StringBuilder();
                s.append((char)byteRead);
                for (int i = 0; i < n-1; i++) {
                    if((byteRead = inputStream.read()) != -1){
                        s.append((char)byteRead);
                    }
                    else break;
                }
                String temp = s.toString();
                if(statistics.containsKey(temp)){
                    statistics.put(temp,statistics.get(temp)+1);
                }
                else{
                    statistics.put(temp,1);
                }
            }
        }
        catch(IOException ex){
            System.out.println("IO Exception");
            return;
            //ex.printStackTrace();
        }
        System.out.println("constructing huffman tree...");
        Node root = ConstructHuffManTree(statistics);
        System.out.println("constructing dictionary...");
        HashMap<String,String> dictionary = createDictionary(root);

        long fileBitLength = 0;
        for(Map.Entry<String,Integer> entry: statistics.entrySet()){
            fileBitLength += (long) dictionary.get(entry.getKey()).length() *entry.getValue();
        }
        int lastByteNBits = (int) fileBitLength%8==0? 8 : (int) (fileBitLength % 8);

        System.out.println("encoding dictionary...");
        String encodeTree = encodeTree(root);
        System.out.println("Compressing file...");
        ConvertAndWriteFile(dictionary, inputFilePath, n, lastByteNBits , encodeTree , outputFilePath);
        System.out.println("compression completed successfully");
    }
    public void DecompressingFile(String inputFilePath){
        //
        File file = new File(inputFilePath);
        int pos = file.getName().lastIndexOf(".");
        if(!file.getName().substring(pos).equals(".hc")){
            System.out.println("the file format is not of type file_name.extension.hc ");
            return;
        }
        String outputFilePath = file.getName();
        if(pos>0 && pos<file.length()-1) {
            outputFilePath = "extracted." + file.getName().substring(0,pos);
        }
        if(file.getParentFile()!=null){
            outputFilePath = file.getParentFile() + "\\" + outputFilePath;
        }
        //
        try(InputStream inputStream = new BufferedInputStream(new FileInputStream(inputFilePath));
            OutputStream outputStream = new BufferedOutputStream(new FileOutputStream(outputFilePath))){
            int lastByteNBit = inputStream.read();
            int byteRead;
            int lastByte;
            StringBuilder encodedTree = new StringBuilder();
            // read encoded tree from file
            System.out.println("reading dictionary...");
            while((byteRead = inputStream.read()) !=-1){
                // the separator
                if(byteRead=='\n'){
                    break;
                }
                else if((char)byteRead!='0'){
                    encodedTree.append((char)byteRead);
                    for (int i = 0; i < byteRead; i++) {
                        int temp;
                        encodedTree.append((char)(temp = inputStream.read()));
                    }
                }
                else{
                    encodedTree.append((char)byteRead);
                }
            }
            // construct the tree from the encoded tree
            System.out.println("constructing HuffMan tree...");
            Node root = constructHuffmanTree(encodedTree);
            Node currentState = root;
            // starting to read the actual file data
            System.out.println("decompressing file...");
            lastByte = inputStream.read();
            while ((byteRead = inputStream.read())!=-1){
                //for each character get its 8-bit binary representation
                String currentByte = String.format("%8s", Integer.toBinaryString(lastByte)).replace(' ', '0');
                for (int i = 0; i < currentByte.length(); i++) {
                    //with each found value 0/1 traverse the tree
                    //if a leaf is found we write its value on the decompressed file and restart from the root
                    if(currentState.isLeaf()){
                        for(int c : currentState.getValue().toCharArray()) {
                            outputStream.write(c);
                        }
                        currentState = root;
                    }
                    if(currentByte.charAt(i)=='1'){
                        currentState = currentState.left;
                    }
                    else{
                        currentState = currentState.right;
                    }
                }
                // lastByte && byteRead work together to stop the process at the last byte in the file as it have a
                // special way to handle because its number of bits is not necessary 8
                lastByte = byteRead;
            }
            if(lastByte!=-1) {
                String currentByte = String.format("%8s", Integer.toBinaryString(lastByte)).replace(' ', '0').substring(0,lastByteNBit);
                for (int i = 0; i < currentByte.length(); i++) {
                    if(currentState.isLeaf()){
                        for(int c : currentState.getValue().toCharArray()) {
                            outputStream.write(c);
                        }
                        currentState = root;
                    }
                    if(currentByte.charAt(i)=='1'){
                        currentState = currentState.left;
                    }
                    else{
                        currentState = currentState.right;
                    }
                }
                if(currentState.isLeaf()){
                    for(int c : currentState.getValue().toCharArray()) {
                        outputStream.write(c);
                    }
                }
            }
        }
        catch (FileNotFoundException e) {
            System.out.println("File Not found");
            //e.printStackTrace();
        } catch (IOException e) {
            System.out.println("IO Exception");
            //e.printStackTrace();
        }
        System.out.println("decompression completed successfully");
    }
    public void printGuide(){
        System.out.println("specify operations to be done using the following format:\n" +
                "(c absolute_file_path n) for compressing where n is the token length\n" +
                "(d absolute_file_path) for decompression");
    }
}
