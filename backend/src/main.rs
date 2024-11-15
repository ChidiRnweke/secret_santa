pub mod schema;
use std::collections::HashSet;

use axum::Json;
use diesel::prelude::*;
use rand::prelude::*;
use schema::user_assignments::buys_for;
use serde::{Deserialize, Serialize};

#[derive(Queryable, Selectable, Insertable)]
#[diesel(check_for_backend(diesel::pg::Pg))]
#[diesel(belongs_to(Session))]
#[diesel(table_name = schema::user_assignments)]
struct UserAssignment {
    id: usize,
    buys_from: String,
    created_at: chrono::NaiveDateTime,
    session_id: String,
}

#[derive(Deserialize)]
struct CreateUserAssignment {
    users: Vec<String>,
}

#[derive(Queryable, Selectable, Insertable)]
#[diesel(check_for_backend(diesel::pg::Pg))]
#[diesel(table_name = schema::session)]
struct Session {
    id: i32,
}

fn derangement<T>(vec: &[T]) -> Vec<T>
where
    T: Clone,
{
    let len = vec.len();
    let mut indices: Vec<usize> = (0..len).collect();
    let mut rng = thread_rng();

    for i in (1..len).rev() {
        let j = rng.gen_range(0..i);
        indices.swap(i, j);
    }

    indices.iter().map(|&i| vec[i].clone()).collect()
}

fn persist_assignment(
    assignment: Vec<UserAssignment>,
    conn: &mut PgConnection,
) -> QueryResult<usize> {
    diesel::insert_into(schema::user_assignments::table)
        .values(&assignment)
        .execute(conn)
}

async fn create_assignment(Json(users): Json<CreateUserAssignment>) -> Json<Vec<UserAssignment>> {
    let assignments = user_list_to_assignments(users.users);
    todo!();
}

fn user_list_to_assignments(users: Vec<String>) -> Vec<UserAssignment> {
    let deranged_users = derangement(&users);
    let assignments = users
        .into_iter()
        .zip(deranged_users)
        .map(|(buyer, user_buys_for)| UserAssignment {
            name: buyer,
            buys_for: user_buys_for,
        })
        .collect();
    assignments
}

fn main() {
    println!("Hello, world!");
}
