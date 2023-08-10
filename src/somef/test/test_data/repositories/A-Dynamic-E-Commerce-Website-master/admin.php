<!DOCTYPE html>
<html>
	<?php 
	session_start();
	if(!(isset($_SESSION['name'])&&isset($_SESSION['email'])))
  	{
    	header('Location: register.php');
  	}
	include "includes/css_header.php"; ?>
<body style="background-color: #EEEEEE;">
	<?php include "includes/header_admin.php"; ?>
	<div class="row margin-left20">

		<div class="col-md-12 text-center">
			<h1 class="font-80px">Admin Pannel</h1>
		</div>
		<br><br><br>
		<a href="admin_orders.php" class="btn btn-lg btn-success margin-left20"> View all Orders</a>
		<br><br><br>
		<?php 
		if(isset($_GET['msg']))
        { 
          if ($_GET['msg']==1)
          {
            echo "<h3 class='text-center text-red'><i>Product has been added</i></h3><br>";
          }
          elseif ($_GET['msg']==2)
          {
            echo "<h3 class='text-center text-red'><i>Product couldnot added</i></h3><br>";
          }
          elseif ($_GET['msg']==11)
          {
            echo "<h3 class='text-center text-red'><i>Product has been Deleted<i></h3><br>";
          }
          elseif ($_GET['msg']==22)
          {
            echo "<h3 class='text-center text-red'><i>Product couldnot be Deleted</i></h3><br>";
          }
        } 
        ?>
		<div class="row">
			<div class="col-md-6">
				<h3 class="font-80px">Add a product To Database</h3>
			</div>
			<div class="col-md-6">
				<form action="upload_product.php" method="POST" enctype="multipart/form-data">
					<label>Product Name</label>
					<input type="text" name="product_name" class="form-control"><br>
					<label>Product Price</label>
					<input type="number" name="product_price" class="form-control"><br>
					<label>Product Description</label>
					<textarea name="product_description" class="form-control"></textarea><br>
					<label>Upload Image</label>
					<input type="file" name="image" class="form-control"><br>
					<input type="submit" value="Add product" class="btn btn-success btn-lg">
				</form>
			</div>
		</div>
		<br><br><br>
		<div class="row">
			<div class="col-md-6">
				<h3 class="font-80px">Delete a product From Database</h3>
			</div>
			<div class="col-md-6">
				<form action="delete_product.php" method="POST">
					<label>Product ID</label>
					<input type="number" name="product_id" class="form-control"><br>
					<input type="submit" value="Delete Product" class="btn btn-success btn-lg">
				</form>
			</div>
		</div>
		
	</div>
</body>
</html>