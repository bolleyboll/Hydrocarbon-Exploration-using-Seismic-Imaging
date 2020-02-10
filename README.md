# [Hydrocarbon-Exploration-using-Seismic-Imaging](https://lit-crag-96627.herokuapp.com/)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Seismic-data interpretation has as it’s main goal the identification of compartments, faults, fault sealing, and trapping mechanism that hold hydrocarbons; it additionally tries to understand the depositional history of the environment to describe the relationship between seismic data and a priori geological information. Finding hydrocarbons through salt detection has been an intricate process, ever since they image salt the first time. Salt bodies form oil traps, which form potential reserves for hydrocarbons. This forms the basis for the motivation behind hydrocarbon sensing via salt detection. Seismic data interpreters are used to interpreting 2D or 3D images that have been heavily processed. In our problem statement, we are dealing with data that is less noisy which is an added advantage. Our solution to the problem is to basically use U-Nets which have shown state of the art results on image segmentation. Each pixel in the image is checked for the presence of salt and further on this is how the proportion of salt in that seismic image is calculated. The energy function is computed by a pixel-wise soft-max over the final feature map combined with the binary cross entropy loss function. Our model boasts an accuracy of 94.7% which is significantly higher than that of in the previous implementations.

You can try it out [here](https://lit-crag-96627.herokuapp.com/).

## Built With
* [Python](https://www.python.org/) - The programming language used.
* [Flask](http://flask.pocoo.org/) - Used as a Web Framework.
* [Bootstrap](https://getbootstrap.com/) - Used for designing webpage elements.

## Authors 
* [Abhishek Varma](https://github.com/abhishekvarma16)
* [Aman Gupta](https://github.com/bolleyboll)
* [Dylan Saldanha](https://github.com/SaberSz)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
