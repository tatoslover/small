#!/usr/bin/env python3
"""
QR Code Generator
Generates a QR code image from a URL or text string.

Run without arguments to open the GUI.

CLI Usage:
    python qr_generator.py "https://example.com"
    python qr_generator.py "Some text" -o my_qr.png
    python qr_generator.py "Some text" -f svg -o my_qr.svg --open
"""

import argparse
import os
import sys
from typing import Any

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------


def check_dependencies() -> None:
    missing = []
    try:
        import qrcode  # noqa: F401
    except ImportError:
        missing.append("qrcode[pil]")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        if "qrcode[pil]" not in missing:
            missing.append("Pillow")
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Core generation logic
# ---------------------------------------------------------------------------


def generate_qr(
    data: str,
    output_path: str,
    fmt: str = "png",
    error_correction: str = "M",
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
) -> str:
    import qrcode
    import qrcode.constants
    import qrcode.image.svg

    levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,  # ~7%
        "M": qrcode.constants.ERROR_CORRECT_M,  # ~15%
        "Q": qrcode.constants.ERROR_CORRECT_Q,  # ~25%
        "H": qrcode.constants.ERROR_CORRECT_H,  # ~30%
    }

    qr = qrcode.QRCode(
        version=None,  # auto-size
        error_correction=levels[error_correction.upper()],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    if fmt.lower() == "svg":
        factory = qrcode.image.svg.SvgPathFillImage
        img: Any = qr.make_image(image_factory=factory)
    else:
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

    img.save(output_path)
    return output_path


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------


def run_gui() -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    try:
        from PIL import Image as _PilImage
        from PIL import ImageTk as _ImageTk

        PIL_AVAILABLE = True
    except ImportError:
        _PilImage = None  # type: ignore[assignment]
        _ImageTk = None  # type: ignore[assignment]
        PIL_AVAILABLE = False

    root = tk.Tk()
    root.title("QR Code Generator")
    root.resizable(False, False)

    # ── Padding helper ──────────────────────────────────────────────────────
    PAD: dict[str, Any] = {"padx": 10, "pady": 6}

    # ── Input frame ─────────────────────────────────────────────────────────
    input_frame = ttk.LabelFrame(root, text="Input", padding=10)
    input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", **PAD)

    ttk.Label(input_frame, text="URL / Text:").grid(row=0, column=0, sticky="w")
    url_var = tk.StringVar()
    url_entry = ttk.Entry(input_frame, textvariable=url_var, width=48)
    url_entry.grid(row=0, column=1, sticky="ew", padx=(6, 0))
    url_entry.focus()

    # ── Output frame ────────────────────────────────────────────────────────
    output_frame = ttk.LabelFrame(root, text="Output", padding=10)
    output_frame.grid(row=1, column=0, columnspan=2, sticky="ew", **PAD)

    # Format selector
    ttk.Label(output_frame, text="Format:").grid(row=0, column=0, sticky="w")
    fmt_var = tk.StringVar(value="png")
    fmt_frame = ttk.Frame(output_frame)
    fmt_frame.grid(row=0, column=1, sticky="w", padx=(6, 0))
    ttk.Radiobutton(fmt_frame, text="PNG", variable=fmt_var, value="png").pack(
        side="left"
    )
    ttk.Radiobutton(fmt_frame, text="SVG", variable=fmt_var, value="svg").pack(
        side="left", padx=(12, 0)
    )

    # Output path
    ttk.Label(output_frame, text="Save as:").grid(
        row=1, column=0, sticky="w", pady=(8, 0)
    )
    save_path_var = tk.StringVar(
        value=os.path.join(os.path.expanduser("~"), "qr_code.png")
    )
    save_entry = ttk.Entry(output_frame, textvariable=save_path_var, width=38)
    save_entry.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(8, 0))

    def browse_save() -> None:
        fmt = fmt_var.get()
        filetypes = (
            [("PNG image", "*.png")] if fmt == "png" else [("SVG file", "*.svg")]
        )
        path = filedialog.asksaveasfilename(
            defaultextension=f".{fmt}",
            filetypes=filetypes,
            initialfile=f"qr_code.{fmt}",
        )
        if path:
            save_path_var.set(path)

    ttk.Button(output_frame, text="Browse…", command=browse_save).grid(
        row=1, column=2, padx=(6, 0), pady=(8, 0)
    )

    def on_format_change(*_: Any) -> None:
        """Keep the file extension in sync with the selected format."""
        current = save_path_var.get()
        base = os.path.splitext(current)[0]
        save_path_var.set(f"{base}.{fmt_var.get()}")

    fmt_var.trace_add("write", on_format_change)

    # ── Preview frame ───────────────────────────────────────────────────────
    preview_frame = ttk.LabelFrame(root, text="Preview", padding=10)
    preview_frame.grid(row=2, column=0, columnspan=2, **PAD)

    PREVIEW_SIZE = 200
    preview_label = ttk.Label(
        preview_frame, text="Preview will appear here.", width=28, anchor="center"
    )
    preview_label.pack()

    # ── Status / Generate ───────────────────────────────────────────────────
    status_var = tk.StringVar()
    status_label = ttk.Label(root, textvariable=status_var, foreground="gray")
    status_label.grid(row=3, column=0, sticky="w", padx=10)

    def generate() -> None:
        data = url_var.get().strip()
        if not data:
            messagebox.showwarning(
                "Missing input", "Please enter a URL or text to encode."
            )
            return

        output_path = save_path_var.get().strip()
        if not output_path:
            messagebox.showwarning("Missing path", "Please choose a save location.")
            return

        fmt = fmt_var.get()

        try:
            generate_qr(data=data, output_path=output_path, fmt=fmt)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        status_var.set(f"Saved: {output_path}")

        # Update preview (PNG only)
        if (
            fmt == "png"
            and PIL_AVAILABLE
            and _PilImage is not None
            and _ImageTk is not None
        ):
            pil_img = _PilImage.open(output_path)
            pil_img.thumbnail((PREVIEW_SIZE, PREVIEW_SIZE))
            photo = _ImageTk.PhotoImage(pil_img)
            preview_label.configure(image=photo, text="")
            preview_label.image = photo  # type: ignore[attr-defined]
        elif fmt == "svg":
            preview_label.configure(
                image="", text="SVG saved — open in a browser to preview."
            )
            preview_label.image = None  # type: ignore[attr-defined]
        else:
            preview_label.configure(
                image="", text="PNG saved (install Pillow for preview)."
            )
            preview_label.image = None  # type: ignore[attr-defined]

    ttk.Button(root, text="Generate QR Code", command=generate).grid(
        row=3, column=1, sticky="e", **PAD
    )

    root.mainloop()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a QR code from text or a URL.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument("data", help="The text or URL to encode.")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path (default: qr_code.png or qr_code.svg).",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="png",
        choices=["png", "svg"],
        help="Output format: png or svg (default: png).",
    )
    parser.add_argument(
        "-e",
        "--error-correction",
        default="M",
        choices=["L", "M", "Q", "H"],
        help=(
            "Error correction level: "
            "L (~7%%), M (~15%%), Q (~25%%), H (~30%%) "
            "(default: M)"
        ),
    )
    parser.add_argument(
        "--box-size",
        type=int,
        default=10,
        help="Pixel size of each QR module (default: 10).",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Quiet zone border width in boxes (default: 4).",
    )
    parser.add_argument(
        "--fill-color",
        default="black",
        help="Module color for PNG output (default: black).",
    )
    parser.add_argument(
        "--back-color",
        default="white",
        help="Background color for PNG output (default: white).",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the generated file after saving.",
    )

    args = parser.parse_args()
    check_dependencies()

    fmt = args.format.lower()
    output_path = os.path.abspath(args.output or f"qr_code.{fmt}")

    print(f"Encoding : {args.data}")
    print(f"Format   : {fmt.upper()}")
    print(f"Output   : {output_path}")

    generate_qr(
        data=args.data,
        output_path=output_path,
        fmt=fmt,
        error_correction=args.error_correction,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill_color,
        back_color=args.back_color,
    )

    print("QR code generated successfully!")

    if args.open:
        import subprocess

        subprocess.run(["open", output_path], check=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # No CLI args → launch GUI; otherwise use CLI
    if len(sys.argv) == 1:
        check_dependencies()
        run_gui()
    else:
        run_cli()
