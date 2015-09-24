<!DOCTYPE html>
<html>
    <head>
        <title>OSXAuditor</title>

        <link rel='stylesheet' type='text/css' href='<?php echo base_url(); ?>css/main.css'>
        <link rel='stylesheet' type='text/css' href='<?php echo base_url(); ?>css/bootstrap.min.css'>

        <!--<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>-->
        <script type="text/javascript" src='<?php echo base_url(); ?>js/jquery.min.js'></script>
        <script type="text/javascript" src='<?php echo base_url(); ?>js/bootstrap.min.js'></script>
        <script type="text/javascript" src='<?php echo base_url(); ?>js/main.js'></script>
    </head>
    <body>
        <div id='header'>
            <div id='title-wrapper'>
                <div id='title'>OS X Auditor</div>
            </div>
            <div id='menu-wrapper' class='container'>
                <div class='row' id='link-row-wrapper'>
                    <div class='menu-item col-xs-1 dropdown' style='width: 90px'>
                        <a class="dropdown-toggle" role="button" id="header-menu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Header
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href='/index.php/Header' id='header-menu-item'>Header</a></li>
                        </ul>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 85px'>
                        <a class="dropdown-toggle" role="button" id="kernel-menu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Kernel
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="/index.php/Kernel" id='kernel-menu-item'>Kernel Extensions</a></li>
                        </ul>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 95px'>
                        <a class="dropdown-toggle" role="button" id="startup-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Startup
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="">System Agents</a></li>
                            <li><a href="#">System Daemons</a></li>
                            <li><a href="#">Third Party Agents</a></li>
                            <li><a href="#">Third Party Daemons</a></li>
                            <li><a href="#">System Scripting Additions</a></li>
                            <li><a href="#">Third Party Scripting Additions</a></li>
                            <li><a href="#">Deprecated System Startup Items</a></li>
                            <li><a href="#">Deprecated Third Party Startup Items</a></li>
                            <li><a href="#">User's Agents</a></li>
                        </ul>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 125px'>
                        <a class="dropdown-toggle" role="button" id="applications-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Applications
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="/index.php/InstalledApps">Installed Applications</a></li>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 125px'>
                        <a class="dropdown-toggle" role="button" id="quarantines-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Quarantines
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="#">Quarantines</a></li>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 115px'>
                        <a class="dropdown-toggle" role="button" id="downloads-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Downloads
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="#">Downloads</a></li>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 105px'>
                        <a class="dropdown-toggle" role="button" id="browsers-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Browsers
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="#">Browsers</a></li>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 90px'>
                        <a class="dropdown-toggle" role="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Airport
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="#">Airport</a></li>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 90px'>
                        <a class="dropdown-toggle" role="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Users
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="#">User Accounts</a></li>
                            <li><a href="#">User Social Accounts</a></li>
                            <li><a href="#">User Mail.app Accounts</a></li>
                            <li><a href="#">Email Accounts</a></li>
                            <li><a href="#">SMTP Accounts</a></li>
                            <li><a href="#">Systems Admins</a></li>
                            <li><a href="#">Systems User's</a></li>
                            <li><a href="#">_amavisd's Account Details</a></li>
                            <li><a href="#">_appleevents's Account Details</a></li>
                            <li><a href="#">_appowner's Account Details</a></li>
                            <li><a href="#">_appserver's Account Details</a></li>
                            <li><a href="#">_ard's Account Details</a></li>
                            <li><a href="#">_assetcache's Account Details</a></li>
                            <li><a href="#">_astris's Account Details</a></li>
                    </div>
                    <div class='menu-item col-xs-1 dropdown' style='width: 125px'>
                        <a class="dropdown-toggle" role="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Logs
                            <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                            <li><a href="#">Event Logs</a></li>
                            <li><a href="#">System Logs</a></li>
                            <li><a href="#">System Logs Timeline</a></li>
                    </div>
                </div>
            </div>
        </div>
         
        <div style='position:absolute;top:80px;left:5px'>
            <?php echo $body; ?>
            <div id='loading-string' style='display: none'>
                <h3>Loading...</h3>
            </div>
        </div>

        <script>
             $(document).ready(function(){
                $('.dropdown-toggle').dropdown();
            });
        </script>
    </body>
</html>