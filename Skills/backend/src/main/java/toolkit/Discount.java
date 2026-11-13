package toolkit;
public final class Discount {
    public static int apply(int total, int percent) {
        if (total < 0 || percent < 0 || percent > 100) throw new IllegalArgumentException("Invalid discount");
        return total * (100 - percent) / 100;
    }
}
