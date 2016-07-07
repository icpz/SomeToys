package com.example.lcdtyph.demo;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

/**
 * Created by lcdtyph on 16/7/5.
 */
public class CATestAdapterMulTest {
    private CATestAdapter mAdapter;

    @Before
    public void setUp() throws Exception {
        mAdapter = new CATestAdapter();
    }

    @Test
    public void mulCase0()throws Exception {
        assertEquals("4 * 5", "20", mAdapter.mul(4, 5));
    }

    @Test
    public void mulCase1()throws Exception {
        assertEquals("0 * 234", "0", mAdapter.mul(0, 234));
    }

    @Test
    public void mulCase2()throws Exception {
        assertEquals("-50.114925 * 284.141718", "-14239.741", mAdapter.mul(-50.114925, 284.141718));
    }

    @Test
    public void mulCase3()throws Exception {
        assertEquals("145.356244 * 65.008579", "9449.40287", mAdapter.mul(145.356244, 65.008579));
    }

    @Test
    public void mulCase4()throws Exception {
        assertEquals("263.829978 * 74.918408", "19765.7219", mAdapter.mul(263.829978, 74.918408));
    }

    @Test
    public void mulCase5()throws Exception {
        assertEquals("251.126564 * 68.549412", "17214.5783", mAdapter.mul(251.126564, 68.549412));
    }

    @Test
    public void mulCase6()throws Exception {
        assertEquals("214.552661 * 216.987970", "46555.3464", mAdapter.mul(214.552661, 216.987970));
    }

    @Test
    public void mulCase7()throws Exception {
        assertEquals("34.754184 * 130.102535", "4521.60744", mAdapter.mul(34.754184, 130.102535));
    }

    @Test
    public void mulCase8()throws Exception {
        assertEquals("123.903915 * 127.361822", "15780.6284", mAdapter.mul(123.903915, 127.361822));
    }

    @Test
    public void mulCase9()throws Exception {
        assertEquals("221.201741 * 114.551221", "25338.9295", mAdapter.mul(221.201741, 114.551221));
    }

}
