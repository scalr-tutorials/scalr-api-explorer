<?php

if ($argc !== 2)
  die("Invalid number of arguments\n");

define("SRCPATH", $argv[1]);
define("LAST_API", "ScalrAPI_2_3_0");
require SRCPATH . "/autoload.inc.php";

$apiClass = new ReflectionClass(LAST_API);

$apiMethods = array();

foreach($apiClass->getMethods() as $methIndex => $method) {
  if (!$method->isPublic() || $method->isConstructor())
    continue;

  $methodName = $method->getName();
  $methodParameters = array();

  // One method we'll ignore
  if ($methodName === "BuildRestServer")
    continue;

  foreach($method->getParameters() as $paramIndex => $parameter) {
    $paramName = $parameter->getName();
    $paramOptional = $parameter->isOptional();

    $methodParameters[$paramName] = array("optional"=>$paramOptional);
  }

  $apiMethods[$methodName] = $methodParameters;
}

print(json_encode($apiMethods, JSON_PRETTY_PRINT));

?>
