package com.example.lcdtyph.demo;

import android.icu.math.BigDecimal;
import android.widget.TextView;

import java.text.DecimalFormat;

/**
 * Created by lcdtyph on 2016/6/30.
 */
public class CalculatorAutomaton {
    enum CalculatorState {FIRSTOP, SECONDOP, HOLDON} // FIRST_OPERATOR etc.

    private CalculatorState mState = CalculatorState.FIRSTOP;
    private Character mOperation = 0;
    private String mOperators[] = new String[2]; // mOperators[0] minus or div mOperators[1]
    private String mTempResult;

    public CalculatorAutomaton() {
        mTempResult = mOperators[0] = mOperators[1] = "0";
    }

    public void pushChar(Character c) {
        String opToView = "";
        if (Character.isDigit(c) || c == '.') {
            if (mState == CalculatorState.HOLDON) {
                mState = CalculatorState.FIRSTOP;
                mOperators[0] = mOperators[1] = "0";
            }

            final int index = mState.ordinal();

            if (mOperators[index] == "0") {
                mOperators[index] = (c == '.' ? "0." : "" + c);
            } else {
                mOperators[index] +=
                        (c == '.' && mOperators[index].indexOf('.') != -1
                            ? "" : c);
            }

            opToView = mOperators[index];

        } else {
            switch (c) {
            case '+':
            case '-':
            case '*':
            case '/':
                if (mState != CalculatorState.FIRSTOP) {
                    mOperators[0] = calc();
                }
                mState = CalculatorState.SECONDOP;
                mOperation = c;
                mOperators[1] = "0";
                opToView = mOperators[0];
                break;

            case '=':
                if (mState != CalculatorState.HOLDON) mState = CalculatorState.HOLDON;
                opToView = calc();
                break;

            case 'C':
                mState = CalculatorState.FIRSTOP;
                mOperators[0] = mOperators[1] = "0";
                opToView = mOperators[0];
                mOperation = 0;

            default:
                break;
            }
        }

        if (opToView.endsWith(".0")) {
            opToView = opToView.substring(0, opToView.length() - 2);
        }
        if (opToView.length() > 10) {
            String fmt = "";
            char fill = '#';
            for (int i = 0; i < 10; ++i) {
                if (opToView.charAt(i) == '.') {
                    fmt = fmt.substring(0, fmt.length() - 1);
                    fmt += "0.";
                    fill = '0';
                } else {
                    fmt += fill;
                }
            }

            opToView = new DecimalFormat(fmt).format(Double.parseDouble(opToView));
        //    opToView = opToView.substring(0, 10);
        }
        int k = opToView.length();
        while (k > 0 && opToView.charAt(--k) == '0')
            ;
        if (k != 0 && opToView.indexOf('.') != -1) opToView = opToView.substring(0, k + 1);
        mTempResult = opToView;
    }

    public String getResult() {
        return mTempResult;
    }

    private String calc(){
        Double result = Double.parseDouble(mOperators[0]);
        switch(mOperation){
        case '+':
            result += Double.parseDouble(mOperators[1]);
            break;

        case '-':
            result -= Double.parseDouble(mOperators[1]);
            break;

        case '*':
            result *= Double.parseDouble(mOperators[1]);
            break;

        case '/':
            result /= Double.parseDouble(mOperators[1]);
            break;

        default:
            break;
        }

        return result <= 999999999 ? result.toString() : "INF";
    }

}
