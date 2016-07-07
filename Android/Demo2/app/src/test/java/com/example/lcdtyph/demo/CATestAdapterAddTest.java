package com.example.lcdtyph.demo;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by lcdtyph on 16/7/4.
 */
public class CATestAdapterAddTest {

    private CATestAdapter mAdapter;

    @Before
    public void setUp() throws Exception {
        mAdapter = new CATestAdapter();
    }

    // Add Test Cases. Total 10
    @Test
    public void addCase0()throws Exception {
        assertEquals("367462.167839 + 198764.433148", "566226.601", mAdapter.add(367462.167839, 198764.433148));
    }

    @Test
    public void addCase1()throws Exception {
        assertEquals("134926.325866 + 105198.844175", "240125.17", mAdapter.add(134926.325866, 105198.844175));
    }

    @Test
    public void addCase2()throws Exception {
        assertEquals("332349.121069 + 42260.454842", "374609.576", mAdapter.add(332349.121069, 42260.454842));
    }

    @Test
    public void addCase3()throws Exception {
        assertEquals("531064.998081 + 383509.011595", "914574.01", mAdapter.add(531064.998081, 383509.011595));
    }

    @Test
    public void addCase4()throws Exception {
        assertEquals("592264.415542 + 159207.088722", "751471.504", mAdapter.add(592264.415542, 159207.088722));
    }

    @Test
    public void addCase5()throws Exception {
        assertEquals("251348.223487 + 411927.631010", "663275.854", mAdapter.add(251348.223487, 411927.631010));
    }

    @Test
    public void addCase6()throws Exception {
        assertEquals("81220.067725 + 596567.302055", "677787.37", mAdapter.add(81220.067725, 596567.302055));
    }

    @Test
    public void addCase7()throws Exception {
        assertEquals("242029.743652 + 692106.728550", "934136.472", mAdapter.add(242029.743652, 692106.728550));
    }

    @Test
    public void addCase8()throws Exception {
        assertEquals("190534.103645 + 108563.866039", "299097.97", mAdapter.add(190534.103645, 108563.866039));
    }

    @Test
    public void addCase9()throws Exception {
        assertEquals("345241.952831 + 376470.487038", "721712.44", mAdapter.add(345241.952831, 376470.487038));
    }
}