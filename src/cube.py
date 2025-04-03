import cadquery as cq
import sys

def generate_cube(cube_number: int, cube_size: float, tube_size: float):
    """
    Generates a 3D cube with text inscriptions on specified faces.

    Parameters:
        cube_number (int): The cube number to engrave on the +Y face.
        cube_size (float): The size of the cube to engrave on the +X face.
        tube_size (float): The tube size to engrave on the -X face.

    Returns:
        CadQuery object representing the final cube.
    """

    # Create the base cube centered at (0,0,0)
    cube = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

    # Prepare formatted text with three significant digits
    cube_number_text = f"{cube_number}"
    cube_size_text = f"{cube_size:.3g}"
    tube_size_text = f"{tube_size:.3g}"

    # Chisel text into the respective faces
    cube = cube.faces("+X").workplane().text(cube_size_text, 0.5, 0.1, cut=True)
    cube = cube.faces("-X").workplane().text(tube_size_text, 0.5, 0.1, cut=True)
    cube = cube.faces("+Y").workplane().text(cube_number_text, 0.5, 0.1, cut=True)

    # Shift the cube so its bottom face is on the build plate (Z = 0)
    cube = cube.translate((0, 0, cube_size / 2))

    return cube

def export_model(model, filename, file_format):
    """
    Exports the given CadQuery model to a file in the specified format.

    Parameters:
        model (cq.Workplane): The CadQuery model to export.
        filename (str): The base name of the output file (without extension).
        file_format (str): The export format, either 'stl' or 'step'.

    Returns:
        None
    """
    if file_format.lower() == "stl":
        cq.exporters.export(model, filename + ".stl")
        print(f"Exported as {filename}.stl")
    elif file_format.lower() == "step":
        cq.exporters.export(model, filename + ".step")
        print(f"Exported as {filename}.step")
    else:
        print("Unsupported format. Use 'stl' or 'step'.")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python src/cube.py <filename> <format> <cube_number> <cube_size> <tube_size>")
        print("Example: python src/cube.py my_cube stl 1 2.397 0.595")
    else:
        filename = sys.argv[1]
        file_format = sys.argv[2]
        cube_number = int(sys.argv[3])
        cube_size = float(sys.argv[4])
        tube_size = float(sys.argv[5])

        cube = generate_cube(cube_number, cube_size, tube_size)
        export_model(cube, filename, file_format)
