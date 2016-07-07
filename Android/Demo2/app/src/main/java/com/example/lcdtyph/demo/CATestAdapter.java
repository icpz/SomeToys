package com.example.lcdtyph.demo;

/**
 * Created by lcdtyph on 16/7/4.
 * 该Class是为方便单元测试而编写的
 */
public class CATestAdapter { // CalculatorAutomatonAdapter
    private CalculatorAutomaton mCA;

    public CATestAdapter() {
        mCA = new CalculatorAutomaton();
    }

    public String add(double a, double b) {
        return operator(a, b, '+');
    }

    public String sub(double a, double b) {
        return operator(a, b, '-');
    }

    public String mul(double a, double b) {
        return operator(a, b, '*');
    }

    public String div(double a, double b) {
        return operator(a, b, '/');
    }
    public String clear() {
        mCA.pushChar('C');
        return mCA.getResult();
    }

    private String operator(double a, double b, char op) {
        String inputSequence = Double.toString(a) + op + Double.toString(b) + "=";
        for (char c : inputSequence.toCharArray()) {
            mCA.pushChar(c);
        }
        return mCA.getResult();
    }
}
