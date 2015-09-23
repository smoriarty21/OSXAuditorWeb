<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Kernel extends CI_Controller {
    public function index() {
        $this->template->load('default', 'kernel');
    }
}
