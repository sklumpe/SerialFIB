from src.Arctis.ArctisDriver import fibsem

fibsem=fibsem()

image=fibsem.take_image_IB()

fibsem.align(image,'ION')