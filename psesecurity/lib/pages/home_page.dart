import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/products.dart';

import '../pages/add_product_page.dart';
import '../widgets/product_item.dart';

import 'dart:math';

class HomePage extends StatefulWidget {
  static const route = "/home";

  @override
  _HomePageState createState() => _HomePageState();
}

class PhotoItem {
  final String image;
  final String name;
  PhotoItem(this.image, this.name);
}

class _HomePageState extends State<HomePage> {
  bool isInit = true;
  bool isLoading = false;

  //---------
  final List<Container> myList = List.generate(
    6,
    (index) {
      return Container(
        height: 50,
        width: 150,
        color: Color.fromARGB(
          255,
          Random().nextInt(256),
          Random().nextInt(256),
          Random().nextInt(256),
        ),
        child:Image(
          image: AssetImage("images/Bella.jpg"),
        ),
      );
    }
  );
  //---------

  //----------
  final List<PhotoItem> _items = [
    PhotoItem(
        "https://images.pexels.com/photos/1772973/pexels-photo-1772973.png?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
        "Stephan Seeber"),
    PhotoItem(
        "https://images.pexels.com/photos/1758531/pexels-photo-1758531.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
        "Liam Gant"),
  ];
  //---------

  @override
  void didChangeDependencies() {
    if (isInit) {
      isLoading = true;
      Provider.of<Products>(context, listen: false).inisialData().then((value) {
        setState(() {
          isLoading = false;
        });
      }).catchError(
        (err) {
          print(err);
          showDialog(
            context: context,
            builder: (context) {
              return AlertDialog(
                title: Text("Error Occured"),
                content: Text(err.toString()),
                actions: [
                  TextButton(
                    onPressed: () {
                      setState(() {
                        isLoading = false;
                      });
                      Navigator.pop(context);
                    },
                    child: Text("Okay"),
                  ),
                ],
              );
            },
          );
        },
      );

      isInit = false;
    }
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    final prov = Provider.of<Products>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text("Caught in 4K"),
        titleTextStyle: TextStyle(
          fontFamily: 'OpenSans',
          fontSize: 18.0,
          color: Colors.white,
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            color: Colors.white,
            onPressed: () => Navigator.pushNamed(context, AddProductPage.route),
          ),
        ],
      ),
      // body: (isLoading)
      //     ? Center(
      //         child: CircularProgressIndicator(),
      //       )
      //     : (prov.allProduct.length == 0)
      //         ? Center(
      //             child: Text(
      //               "No Data",
      //               style: TextStyle(
      //                 fontSize: 25,
      //               ),
      //             ),
      //           )
      //         : ListView.builder(
      //             itemCount: prov.allProduct.length,
      //             itemBuilder: (context, i) => ProductItem(
      //               prov.allProduct[i].id,
      //               prov.allProduct[i].title,
      //               prov.allProduct[i].price,
      //               prov.allProduct[i].updatedAt,
      //             ),
      //           ),
      //----------At least 1 pic--------------
      // body: Center(
      //   child: Container(
      //     width: 350,
      //     height: 500,
      //     color: Colors.pinkAccent,
      //     child:Image(
      //       image: AssetImage("images/Bella.jpg"),
      //       //image: NetworkImage("url"),
      //   )
      // )
      // )

      //--------------Grid View-------------------
      body: GridView(
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          crossAxisSpacing: 20,
          mainAxisSpacing: 10,
        ),
        children: myList,
      )
      //----------

    );
  }
}
