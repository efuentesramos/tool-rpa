use lsv_rpa::win_tools::mouse::*;
use std::thread;
use std::time::Duration;


 fn main() {
    let pos_xy:ScreenXY;
    let cursor_info:InfoCursor;
    let info_cut:InfoCutout;

    let duration = Duration::from_millis(3000);
   
    thread::sleep(duration);

   // mouse_click(1);
    /* mouse_move(0,0);
    thread::sleep(duration);
    mouse_move(683,384);
    thread::sleep(duration);*/
    //mouse_move(1366,0);
    //thread::sleep(duration);
    
    pos_xy = get_cursor_pos();
    println!("Las Coordenadas del Mouse Son X: {} Y:{}",pos_xy.x,pos_xy.y);
    thread::sleep(duration);
    cursor_info=get_cursor_info();
    println!("La informacion del cursor es: {:?}",cursor_info);

    info_cut=make_screen_cutouts(280,100,r#"prueba_recortes7"#);
    println!("La informacion del recorte es : {:?}",info_cut);
    println!("Hello, world!");
   
}
