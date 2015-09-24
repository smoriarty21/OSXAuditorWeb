<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class InstalledApps extends CI_Controller {
    public function index() {
        $this->template->load('default', 'installedapps');
    }
}
