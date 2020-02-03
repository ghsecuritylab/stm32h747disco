#include "unity.h"
#include "App.h"

void setUp(void)
{
}

void tearDown(void)
{
}

void test_APP_sum()
{
    int32_t sum = APP_sum(3, 1);
    TEST_ASSERT_EQUAL_INT(sum, 4);
}
