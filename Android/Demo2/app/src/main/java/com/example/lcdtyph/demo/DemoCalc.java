package com.example.lcdtyph.demo;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.GestureDetector;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterViewFlipper;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.GridView;
import android.widget.LinearLayout;
import android.widget.SimpleAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DemoCalc extends AppCompatActivity
                        implements GestureDetector.OnGestureListener {

    CalculatorAutomaton mCalcAuto;
    AdapterViewFlipper mFlipper;
    GestureDetector mDetector;
    TextView mView;
    String[] chars = new String[] {
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
            };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_demo_calc);
        mCalcAuto = new CalculatorAutomaton();
        mFlipper = (AdapterViewFlipper)findViewById(R.id.flipper);
        mDetector = new GestureDetector(this, this);
        mView = (TextView) findViewById(R.id.view);

        final View.OnClickListener btnCallback = new View.OnClickListener() {
                            @Override
                            public void onClick(View view) {
                                mCalcAuto.pushChar(((Button)view).getText().charAt(0));
                                mView.setText(mCalcAuto.getResult());
                            }
                        };

        BaseAdapter adapter = new BaseAdapter() {
            @Override
            public int getCount() {
                return chars.length;
            }

            @Override
            public Object getItem(int pos) {
                return pos;
            }

            @Override
            public long getItemId(int pos) {
                return pos;
            }

            @Override
            public View getView(int pos, View convertView, ViewGroup parent){
                GridView gridView = new GridView(DemoCalc.this);
                gridView.setGravity(Gravity.CENTER);
                gridView.setNumColumns(4);
                gridView.setHorizontalSpacing(1);
                gridView.setVerticalSpacing(1);
                gridView.setStretchMode(GridView.STRETCH_COLUMN_WIDTH);
                LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT);
                params.gravity = Gravity.CENTER_HORIZONTAL;

                gridView.setLayoutParams(params);
                List<Map<String, Object>> listItems = new ArrayList<>();

                for (int i = 0; i < chars.length; ++i) {
                    Map<String, Object> listItem = new HashMap<>();
                    listItem.put("btn", chars[(i + pos) % chars.length]);
                    listItems.add(listItem);
                }

                SimpleAdapter simpleAdapter = new SimpleAdapter(DemoCalc.this,
                        listItems, R.layout.activity_gridview_cell,
                        new String[]{"btn"}, new int[]{R.id.cellbtn}){

                    @Override
                    public View getView(int position, View convertView, ViewGroup parent){
                        View v = super.getView(position, convertView, parent);

                        Button btn = (Button)v.findViewById(R.id.cellbtn);
                        btn.setOnClickListener(btnCallback);
                        return v;
                    }
                };
                gridView.setAdapter(simpleAdapter);
                return gridView;
            }
        };

        mFlipper.setAdapter(adapter);
        findViewById(R.id.btnClr).setOnClickListener(btnCallback);
    }

    @Override
    public boolean onTouchEvent(MotionEvent me) {
        return mDetector.onTouchEvent(me);
    }

    @Override
    public void onShowPress(MotionEvent e) {
    }

    @Override
    public void onLongPress(MotionEvent e) {
    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        return false;
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float x, float y) {
        return false;
    }

    @Override
    public boolean onFling(MotionEvent e1, MotionEvent e2, float x, float y) {
        if (e2.getX() - e1.getX() > 120) { // left to right
            mFlipper.setInAnimation(this, R.animator.slide_left_in);
            mFlipper.setOutAnimation(this, R.animator.slide_right_out);
            mFlipper.showPrevious();
        } else if (e2.getX() - e1.getX() < -120) {
            mFlipper.setInAnimation(this, R.animator.slide_right_in);
            mFlipper.setOutAnimation(this, R.animator.slide_left_out);
            mFlipper.showNext();
        }

        return true;
    }

    @Override
    public boolean onDown(MotionEvent e) {
        return false;
    }
}
