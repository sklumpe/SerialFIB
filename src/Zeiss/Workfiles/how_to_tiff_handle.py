
def on_load_image(self):
    self.fname = QtWidgets.QFileDialog.getOpenFileName(self,"Load SEM image", filter="Images (*.tif)")[0]
    img, pix = tiff_handle.read_tiff(self.fname)
    image_pixel_size = tiff_handle.get_tiff_info(self.fname)["AP_IMAGE_PIXEL_SIZE"].split()
    tilt_angle = tiff_handle.get_tiff_info(self.fname)["AP_STAGE_AT_T"].split()
    self.angle = float(tilt_angle[0])
    if image_pixel_size[1] == "nm": self.pix = float(image_pixel_size[0])*1e-9
    elif image_pixel_size[1] == "µm": self.pix = float(image_pixel_size[0])*1e-6
    
    print(self.pix, self.angle)
    self.featured_img = img
    print(f"Image {self.fname} has been loaded.")
    if self.fname != "":
        self.ax.clear()
        self.ax.imshow(self.featured_img, cmap="gray")
        self.ax.set_axis_off()
        #self.add_line()
        self.canvas.draw()
        self.num_tilt_angle.setValue(self.angle)
        #self.get_pixel_pos()