package com.example.lcdtyph.demo;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

/**
 * Created by lcdtyph on 16/7/5.
 */
public class CATestAdapterSubTest {
    private CATestAdapter mAdapter;

    @Before
    public void setUp() throws Exception {
        mAdapter = new CATestAdapter();
    }


    @Test
    public void subCase0()throws Exception {
        assertEquals("468973.773687 - 271566.904228", "197406.869", mAdapter.sub(468973.773687, 271566.904228));
    }

    @Test
    public void subCase1()throws Exception {
        assertEquals("7180.090959 - 117766.723014", "-110586.63", mAdapter.sub(7180.090959, 117766.723014));
    }

    @Test
    public void subCase2()throws Exception {
        assertEquals("577465.504449 - 138526.597963", "438938.906", mAdapter.sub(577465.504449, 138526.597963));
    }

    @Test
    public void subCase3()throws Exception {
        assertEquals("726455.517428 - 728527.143086", "-2071.6257", mAdapter.sub(726455.517428, 728527.143086));
    }

    @Test
    public void subCase4()throws Exception {
        assertEquals("691928.436910 - 578821.136746", "113107.3", mAdapter.sub(691928.436910, 578821.136746));
    }

    @Test
    public void subCase5()throws Exception {
        assertEquals("419356.176973 - 698969.432369", "-279613.26", mAdapter.sub(419356.176973, 698969.432369));
    }

    @Test
    public void subCase6()throws Exception {
        assertEquals("134472.118109 - 123097.017191", "11375.1009", mAdapter.sub(134472.118109, 123097.017191));
    }

    @Test
    public void subCase7()throws Exception {
        assertEquals("58028.875574 - 340833.980969", "-282805.11", mAdapter.sub(58028.875574, 340833.980969));
    }

    @Test
    public void subCase8()throws Exception {
        assertEquals("538485.285366 - 359298.569158", "179186.716", mAdapter.sub(538485.285366, 359298.569158));
    }

    @Test
    public void subCase9()throws Exception {
        assertEquals("117992.413753 - 513801.122718", "-395808.71", mAdapter.sub(117992.413753, 513801.122718));
    }

}
