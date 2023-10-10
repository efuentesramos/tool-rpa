use windows::{
    Win32::UI::Input::KeyboardAndMouse::*,
    Win32::UI::WindowsAndMessaging::*, Win32::Foundation::*,
};
use screenshots::Screen;

use core::mem;
#[derive(Debug)]
pub struct ScreenXY {
    pub x: i32,
    pub y: i32,
}
#[derive(Debug)]
pub struct InfoCursor{
    pub x: i32,
    pub y: i32, 
    pub cursor_type:isize,
}

#[derive(Debug)]
pub struct InfoCutout{
    pub x: i32,
    pub y: i32, 
    pub cursor_type:isize,
    pub height:u32,
    pub width: u32,
}

pub fn make_screen_cutouts(width_area:u32,height_area:u32,save_path:&str)->InfoCutout{
    
    let screens = Screen::all().unwrap();
    let cursor_info:InfoCursor;
    let info_cutout:InfoCutout;
    cursor_info=get_cursor_info();

    
    for screen in screens {
       // println!("capturer {screen:?}");
        let mut image = screen.capture().unwrap();
        // image
        //     .save(format!("target/{}.png", screen.display_info.id))
        //     .unwrap();

        image = screen.capture_area(cursor_info.x, cursor_info.y, width_area, height_area).unwrap();
        image
            .save(format!("target/{}.png", save_path))
            .unwrap();
    }
    info_cutout=InfoCutout { x:(cursor_info.x),y:(cursor_info.y), cursor_type: (cursor_info.cursor_type),height:(height_area),width:(width_area) };
    info_cutout

}
pub fn get_cursor_info()->InfoCursor{
    
    let info_cursor: InfoCursor;
    
    let cursor=unsafe{GetCursor()};

    let  cursor_pos = POINT{
        x:0,
        y:0,
    };
     
    let mut cursor_info =CURSORINFO{
        cbSize: 24,
        flags:CURSOR_SHOWING,
        hCursor:cursor,
        ptScreenPos:cursor_pos,

    };
   
    unsafe{ let _= GetCursorInfo(&mut cursor_info);}
        
    info_cursor=InfoCursor { x:(cursor_info.ptScreenPos.x),y:(cursor_info.ptScreenPos.y), cursor_type: (cursor_info.hCursor.0) };
    info_cursor  

}

pub fn get_cursor_pos ()->ScreenXY{

    let mut pos_xy=ScreenXY{
        x:0,
        y:0,
    };
    
    let mut cursor_pos = POINT{
        x:0,
        y:0,
    };
   
    unsafe {
       
        let _= GetCursorPos(&mut cursor_pos);
       
    }

    pos_xy.x = cursor_pos.x;
    pos_xy.y = cursor_pos.y;

    pos_xy

}

pub fn mouse_event_down(type_click:u8){
    println!("Entro la funcion mouse_event_down de validacion con tipo de click");
    let type_input= INPUT_TYPE{
        0:0, //input by Mouse
    };

    if (type_click >0) & (type_click<4) {
        //println!("IF");
        println!("Entro al IF mouse_event_down de validacion con tipo de click : {}",type_click);
        let flag = match type_click {
            1=>MOUSEEVENTF_RIGHTDOWN,
            2=>MOUSEEVENTF_LEFTDOWN,
            3=>MOUSEEVENTF_MIDDLEDOWN,
            _ =>MOUSEEVENTF_LEFTDOWN,
        };
        let mouse_input= MOUSEINPUT {
            dx: 0,
            dy: 0,
            mouseData: 0,
            dwFlags: flag,
            time: 0,
            dwExtraInfo: mem::size_of::<INPUT>(),
        };
    
        let type_input_0= INPUT_0{
            mi:mouse_input,
        };
    
        let entrada=[INPUT{
            r#type : type_input,
            Anonymous :type_input_0,
        }];
    
        unsafe {
            SendInput(&entrada,40);
        }
    }

}

pub fn mouse_event_up(type_click:u8){
    println!("Entro la funcion mouse_event_up de validacion con tipo de click");
    let type_input= INPUT_TYPE{
        0:0, //input by Mouse
    };

    if (type_click >0) & (type_click<4) {
        //println!("IF");
        println!("Entro IF funcion mouse_event_up de validacion con tipo de click : {}",type_click);
        let flag = match type_click {
            1=>MOUSEEVENTF_RIGHTUP,
            2=>MOUSEEVENTF_LEFTUP,
            3=>MOUSEEVENTF_MIDDLEUP,
            _ =>MOUSEEVENTF_LEFTUP,
        };
        let mouse_input= MOUSEINPUT {
            dx: 0,
            dy: 0,
            mouseData: 0,
            dwFlags: flag,
            time: 0,
            dwExtraInfo: mem::size_of::<INPUT>(),
        };
    
        let type_input_0= INPUT_0{
            mi:mouse_input,
        };
    
        let entrada=[INPUT{
            r#type : type_input,
            Anonymous :type_input_0,
        }];
    
        unsafe {
            SendInput(&entrada,40);
        }
    }
    
}

pub fn mouse_click(type_click:u8) {

    if (type_click >0) & (type_click<4) {
        mouse_event_down(type_click);
        mouse_event_up(type_click);
        println!("Funcion Click");
    }
}

pub fn mouse_move(dx:i32,dy:i32){
    
    const DISPLAY_SURFACE :u16 =65535;

    unsafe {
        let width_screen: i32  = GetSystemMetrics(SM_CXVIRTUALSCREEN);
        let heigh_screen: i32  = GetSystemMetrics(SM_CYVIRTUALSCREEN);
        let cx=dx*(DISPLAY_SURFACE as i32)/width_screen;
        let cy=dy*(DISPLAY_SURFACE as i32)/heigh_screen;
        let type_input= INPUT_TYPE{
            0:0, //input by Mouse
        };

    let mouse_input= MOUSEINPUT {
        dx: cx,
        dy: cy,
        mouseData: 0,
        dwFlags: MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        time: 0,
        dwExtraInfo: mem::size_of::<INPUT>(),
    };

    let type_input_0= INPUT_0{
        mi:mouse_input,
    };

    let entrada=[INPUT{
        r#type : type_input,
        Anonymous :type_input_0,
    }];
    SendInput(&entrada,40);

    }

}