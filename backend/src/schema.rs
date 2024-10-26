diesel::table! {
    user_assignments (id) {
        id -> Int4,
        name -> VarChar,
        buys_for -> VarChar,
        session_id -> Int4,
    }
}

diesel::table! {
    session (id) {
        id -> Int4,
        created_at -> Timestamp,
    }
}
