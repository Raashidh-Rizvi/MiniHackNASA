package toolkit;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
class DiscountTest {
    interface RateProvider { int percent(); }
    @Test void boundaries() {
        assertEquals(80, Discount.apply(100,20)); assertEquals(100,Discount.apply(100,0));
        assertEquals(0, Discount.apply(100,100)); assertEquals(0,Discount.apply(0,20));
        assertThrows(IllegalArgumentException.class,()->Discount.apply(-1,20));
        assertThrows(IllegalArgumentException.class,()->Discount.apply(100,-1));
        assertThrows(IllegalArgumentException.class,()->Discount.apply(100,101));
    }
    @Test void isolatedDependency() {
        RateProvider rates=mock(RateProvider.class); when(rates.percent()).thenReturn(10);
        assertEquals(90,Discount.apply(100,rates.percent())); verify(rates).percent();
    }
}
