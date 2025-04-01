use warp::ws::{Message, WebSocket};
use warp::Filter;
use futures::{SinkExt, StreamExt};

pub fn ws_route() -> impl warp::Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
    warp::path("ws")
        .and(warp::ws())
        .and_then(handle_ws)
}

async fn handle_ws(ws: warp::ws::Ws) -> Result<impl warp::Reply, warp::Rejection> {
    Ok(ws.on_upgrade(handle_connection))
}

async fn handle_connection(ws: WebSocket) {
    let (mut tx, mut rx) = ws.split();

    // Echo any text messages back
    while let Some(result) = rx.next().await {
        if let Ok(msg) = result {
            if msg.is_text() || msg.is_binary() {
                if tx.send(msg).await.is_err() {
                    // client disconnected
                    break;
                }
            }
        } else {
            break;
        }
    }
}
