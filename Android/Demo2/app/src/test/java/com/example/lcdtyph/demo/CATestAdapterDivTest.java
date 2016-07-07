package com.example.lcdtyph.demo;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;


/**
 * Created by lcdtyph on 16/7/5.
 */
public class CATestAdapterDivTest {

    private CATestAdapter mAdapter;

    @Before
    public void setUp() throws Exception {
        mAdapter = new CATestAdapter();
    }


    @Test
    public void divCase0()throws Exception {
        assertEquals("0 / 722321.099778", "0", mAdapter.div(0, 722321.099778));
    }

    @Test
    public void divCase1()throws Exception {
        assertEquals("74998.648412 / 109232.515890", "0.68659637", mAdapter.div(74998.648412, 109232.515890));
    }

    @Test
    public void divCase2()throws Exception {
        assertEquals("426706.484009 / 181568.051522", "2.35011876", mAdapter.div(426706.484009, 181568.051522));
    }

    @Test
    public void divCase3()throws Exception {
        assertEquals("432105.005183 / 413656.216757", "1.04459933", mAdapter.div(432105.005183, 413656.216757));
    }

    @Test
    public void divCase4()throws Exception {
        assertEquals("210993.676716 / 678066.322345", "0.31116967", mAdapter.div(210993.676716, 678066.322345));
    }

    @Test
    public void divCase5()throws Exception {
        assertEquals("357470.273310 / 798369.753602", "0.44775027", mAdapter.div(357470.273310, 798369.753602));
    }

    @Test
    public void divCase6()throws Exception {
        assertEquals("104965.966468 / 517050.630560", "0.20300907", mAdapter.div(104965.966468, 517050.630560));
    }

    @Test
    public void divCase7()throws Exception {
        assertEquals("613988.625300 / 620576.874575", "0.98938367", mAdapter.div(613988.625300, 620576.874575));
    }

    @Test
    public void divCase8()throws Exception {
        assertEquals("577574.076753 / 0", "INF", mAdapter.div(577574.076753, 0));
    }

    @Test
    public void divCase9()throws Exception {
        assertEquals("332237.086461 / 152642.734891", "2.17656665", mAdapter.div(332237.086461, 152642.734891));
    }

}
