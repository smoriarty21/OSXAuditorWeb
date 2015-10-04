<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Quarantines extends CI_Controller {
    public function index() {
        $this->template->load('default', 'quarantines');
    }
}
