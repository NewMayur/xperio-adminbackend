use warp::Filter;
use tokio::signal;

mod api;
mod websocket;
mod messaging;
mod db;
mod config;

#[tokio::main]
async fn main() {
    // Load configuration (e.g., using dotenv)
    let config = config::Config::from_env().expect("Invalid or missing config");

    // Connect to database if needed
    db::init(&config.database_url).await.expect("DB init failed");

    // Initialize NATS client
    let nats_client = messaging::nats_client::NatsClient::new(&config.nats_url).await;

    // Build API filters (example: authentication endpoints)
    let api_routes = api::auth::routes(nats_client.clone())
        .or(api::rooms::routes());
        /* .or(other routes) */;

    // Build WebSocket route(s) for real-time chat or notifications.
    let ws_route = websocket::chat::ws_route();

    // Merge API and WebSocket routes
    let routes = api_routes.or(ws_route);

    println!("Rust server listening on {}", config.server_addr);

    // Start the Warp server.
    warp::serve(routes)
        .run(config.server_addr.parse().unwrap())
        .await;
}
