<?php
	session_start();
	if(!(isset($_SESSION['name'])&&isset($_SESSION['email'])))
  	{
   		header('Location: register.php');
  	}
?>
<!DOCTYPE html>
<html>
	<?php
		if(($_SESSION['email']=="admin@mangola.com"))
        {
          include "includes/header_admin.php";
        }
        else
        {
        	header('Location: index.php');
        }
		include "includes/css_header.php";
		include "includes/dbconnect.php";
	?>
<body>
	<div class="container">
		<div class="row">
			<div class="col-md-12">
				<h1 class="text-center font-80px"> The Orders </h1>
			</div>
		</div>
		<div class="row">
			<?php
				$query="SELECT * FROM `orders` o JOIN `products` p ON o.`product_id`=p.`product_id` JOIN `users` u ON o.`user_id`=u.`user_id` JOIN `details` d ON o.`user_id`=d.`user_id`";
				$result=mysqli_query($connection,$query);
				while($row=mysqli_fetch_assoc($result))
				{
				echo'<div class="col-md-3">
						<div class="product-tab">
							<p><b> User Name: '.$row['name'].'<br>
							User ID: '.$row['user_id'].'<br>
							Product Name: '.$row['product_name'].'<br>
							Product ID: '.$row['product_id'].'<br>
							Quantity: '.$row['quantity'].'<br>
							Address: '.$row['address'].'<br>
							Order ID: '.$row['order_id'].'<br>
							</b></p>
							
						</div>
					</div>';
				}
			?>
		</div>		
	</div>
</body>
</html>