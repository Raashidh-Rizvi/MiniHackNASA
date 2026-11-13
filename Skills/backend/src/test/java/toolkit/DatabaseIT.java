package toolkit;
import org.junit.jupiter.api.Test;
import org.testcontainers.containers.PostgreSQLContainer;
import java.sql.DriverManager;
import static org.junit.jupiter.api.Assertions.*;
class DatabaseIT {
    @Test void realDatabaseRoundTrip() throws Exception {
        try (var db=new PostgreSQLContainer<>("postgres:17-alpine")) {
            db.start();
            try(var con=DriverManager.getConnection(db.getJdbcUrl(),db.getUsername(),db.getPassword());var stmt=con.createStatement()) {
                stmt.execute("CREATE TABLE tenants(id INT PRIMARY KEY, name TEXT NOT NULL)");
                stmt.execute("INSERT INTO tenants VALUES(1,'alpha')");
                try(var rows=stmt.executeQuery("SELECT name FROM tenants WHERE id=1")) {assertTrue(rows.next());assertEquals("alpha",rows.getString(1));}
            }
        }
    }
}
