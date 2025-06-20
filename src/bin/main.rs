// fig 1.3-DFT 1.0, page 12
//
// 10 REM *** DFT 1.0 - GENERATE SQUARE WAVE ***
// 12 INPUT "NUMBER OF TERMS";N
// 20 PI = 3.14159265358#
// 30 FOR I = 0 TO 2*PI STEP PI/8
// 32 Y=0
// 40 FOR J=1 TO N STEP 2: Y=Y+SIN(J*I) /J: NEXT J
// 50 PRINT Y
// 60 NEXT I
// 70 END

//use gnuplot::{AxesCommon, Caption, Figure};
use gnuplot::{AxesCommon, Caption, Figure, PointSymbol};
use std::f64::consts::PI;

use std::io::Write;

fn get_input() -> String {
    let mut s = String::new();
    std::io::stdin()
        .read_line(&mut s)
        .expect("Failed to read line");
    String::from(s.trim())
}

/// Prompt the user for input, parse as type T
pub fn get_number<T: std::str::FromStr>(msg: &str) -> T {
    loop {
        println!("{msg}");
        std::io::stdout().flush().unwrap();
        let input: String = get_input();
        if let Ok(num) = input.trim().parse::<T>() {
            return num;
        } else {
            println!("Invalid input. Please enter a valid number.");
        };
    }
}

#[derive(Clone, Copy)]
enum SeriesType {
    SquareWave,       // sin(jx)/j
    SmoothedSine,     // sin(jx)/j²
    TriangleWave,     // cos(jx)/j²
    InvertedTriangle, // -cos(jx)/j²
    SpecialCosine,    // -(-1)^j * cos(jx)/(4j² - 1)
}

impl SeriesType {
    fn label(self) -> &'static str {
        match self {
            SeriesType::SquareWave => "Square Wave: sin(jx)/j",
            SeriesType::SmoothedSine => "Smoothed Sine: sin(jx)/j²",
            SeriesType::TriangleWave => "Triangle Wave: cos(jx)/j²",
            SeriesType::InvertedTriangle => "Inverted Triangle: -cos(jx)/j²",
            SeriesType::SpecialCosine => "Special Cosine: -(-1)^j * cos(jx)/(4j² - 1)",
        }
    }

    fn compute_term(self, x: f64, j: f64) -> f64 {
        match self {
            SeriesType::SquareWave => (j * x).sin() / j,
            SeriesType::SmoothedSine => (j * x).sin() / (j * j),
            SeriesType::TriangleWave => (j * x).cos() / (j * j),
            SeriesType::InvertedTriangle => -(j * x).cos() / (j * j),
            SeriesType::SpecialCosine => {
                -(-1.0f64).powi(j as i32) * (j * x).cos() / (4.0 * j * j - 1.0)
            }
        }
    }
}

/// Plots a Fourier series function over [0, 2π]
fn plot_series(series: SeriesType, n_terms: u32, step_size: usize) {
    let label = match step_size {
        1 => "ALL",
        2 => "ODD",
        _ => "Unexpected",
    };

    const TICKS_PER_PI: usize = 16;
    let mut x_vals = Vec::new();
    let mut y_vals = Vec::new();

    for i in 0..=2 * TICKS_PER_PI {
        let x = i as f64 * PI / TICKS_PER_PI as f64;
        let y: f64 = (1..=n_terms)
            .step_by(step_size)
            .map(|j| series.compute_term(x, j as f64))
            .sum();
        x_vals.push(x);
        y_vals.push(y);
    }

    let mut fg = Figure::new();
    fg.axes2d()
        .lines_points(
            &x_vals,
            &y_vals,
            &[
                Caption(&format!(
                    "{}, {label} terms, #terms={n_terms}",
                    series.label()
                )),
                PointSymbol('o'),
            ],
        )
        .set_x_label("x", &[])
        .set_y_label("y", &[]);

    fg.show().unwrap();
}

fn main() {
    let max_n = get_number::<u32>("NUMBER OF TERMS?");

    for n in (1..=max_n).step_by(2) {
        plot_series(SeriesType::SquareWave, n, 2);
    }
}
