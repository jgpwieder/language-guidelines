use actix_web::{
    get, 
    post, 
    put,
    error::ResponseError,
    web::Path,
    web::Json,
    web::Data,
    HttpResponse,
    http::{header::ContentType, StatusCode}
};
use serde::{Serialize, Deserialize};
use derive_more::{Display};

#[derive(Deserialize, Serialize)]
pub struct TaskId {
    task_id: String,
}

// These are the handler functions, and they can return the following vlaues:
//  - struct that implements a responder
//  - result which the succes value implements a reponder 
#[get("/task/{task_id}")]
pub async fn get_task(task_id: Path<TaskId>) -> actix_web::Result<Json<String>> {
    let task_id_value = task_id.into_inner().task_id;
    Ok(Json(task_id_value))
}
