import java.awt.color.ColorSpace;

public class ColorConverter {


    public static float[] convertRGBtoXYZ(int r, int g, int b) {
        if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
            throw new IllegalArgumentException("RGB values must be between 0 and 255.");
        }

        ColorSpace cs = ColorSpace.getInstance(ColorSpace.CS_sRGB);
        float[] rgb = new float[]{r / 255f, g / 255f, b / 255f};
        return cs.toCIEXYZ(rgb);
    }

    public static void main(String[] args) {
        float[] xyz = convertRGBtoXYZ(255, 0, 0);
        System.out.println("XYZ: " + xyz[0] + ", " + xyz[1] + ", " + xyz[2]);
    }
}