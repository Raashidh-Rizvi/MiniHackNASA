package toolkit;
import com.github.tomakehurst.wiremock.WireMockServer;
import org.junit.jupiter.api.Test;
import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static io.restassured.RestAssured.*;
class ProviderTest {
    @Test void providerFailuresAndAuthorization() {
        WireMockServer server=new WireMockServer(0); server.start();
        try {
            server.stubFor(get(urlEqualTo("/payment")).willReturn(aResponse().withStatus(503).withFixedDelay(50)));
            server.stubFor(get(urlEqualTo("/private")).willReturn(aResponse().withStatus(401)));
            server.stubFor(get(urlEqualTo("/health")).willReturn(okJson("{\"status\":\"ok\"}")));
            given().baseUri(server.baseUrl()).when().get("/payment").then().statusCode(503);
            given().baseUri(server.baseUrl()).when().get("/private").then().statusCode(401);
            given().baseUri(server.baseUrl()).when().get("/health").then().statusCode(200).body("status",org.hamcrest.Matchers.equalTo("ok"));
        } finally {server.stop();}
    }
}
