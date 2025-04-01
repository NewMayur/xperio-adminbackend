use async_nats::{Client, ConnectOptions};
use std::sync::Arc;

#[derive(Clone)]
pub struct NatsClient {
    client: Arc<Client>,
}

impl NatsClient {
    pub async fn new(nats_url: &str) -> Self {
        let client = async_nats::connect(nats_url).await.expect("NATS connection failed");
        Self { client: Arc::new(client) }
    }

    pub async fn publish_message(&self, subject: &str, payload: &[u8]) {
        let _ = self.client.publish(subject.to_string(), payload.into()).await;
    }

    pub async fn subscribe(&self, subject: &str) -> async_nats::Subscriber {
        self.client.subscribe(subject.to_string()).await.expect("Failed to subscribe")
    }
}
