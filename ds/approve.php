<?php

if(isset($_POST['approve']) && $_POST['approve'] == 1){

	$command = escapeshellcmd('python ./figmaIntegration.py');
	$output = shell_exec($command);
	header('Location: http://totvs.ds.com/');
	exit;
}

?>
<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="./components.css?v=<?php echo time(); ?>">
	<title>Design System::UX Lab</title>

	<script type="text/javascript">
		function goBack(){
			window.history.back();
		}
	</script>
</head>
<body>
	
	<h1>Design System - UX Lab [Aprovação]</h1>

	<div>

		<form method="POST" >
			<input type="hidden" name="approve" value="1">
			<p>Legal! As alterações do Design System estão prontas para serem aplicadas?</p>
			<p>Se estiverem basta clicar no botão abaixo!</p>

			<div>
				<button type="submit" class="ds button-primary">Aprovar Design System</button>
				<button type="button" class="ds button-secondary" onclick="goBack();">Voltar</button>
			</div>
		</form>
		

	</div>

</body>
</html>