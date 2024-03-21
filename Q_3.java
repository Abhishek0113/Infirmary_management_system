package Exp_2;

import java.util.Scanner;
public class Q_3 {
    public static void main(String args[]) {
        int count, temp;
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter number of marks: ");
        count = sc.nextInt();
        int num[] = new int[count];
        System.out.println("Enter array elements:");
        for (int i = 0; i < count; i++) {
            num[i] = sc.nextInt();
        }
        for (int i = 0; i < count; i++) {
            for (int j = i + 1; j < count; j++) {
                if (num[i] > num[j]) {
                    temp = num[i];
                    num[i] = num[j];
                    num[j] = temp;
                }
            }
        }
        System.out.print("Array Elements in Ascending Order:");
        for (int i = 0; i < count - 1; i++) {
            System.out.print(num[i] + ", ");
        }
        System.out.println(num[count - 1]);
        System.out.println();
        for (int i = 0; i < count; i++) {
            if (num[i] >= 0 && num[i] <= 39) {
                System.out.println(num[i] + "" + " FAIL");

            } else if (num[i] >= 40 && num[i] <= 50) {
                System.out.println(num[i] + "" + " PASS");

            } else if (num[i] >= 51 && num[i] <= 75) {
                System.out.println(num[i] + " " + "MERIT");

            } else {
                System.out.println(num[i] + "" + " DISTINCTION ");
            }
        }
    }
}
